"""
The Continuum Report - Ollama LLM Client

A robust client for interacting with Ollama for LLM inference.
Features streaming responses, retry logic, and memory management.

Usage:
    from continuum_report.lib.ollama_client import OllamaClient

    client = OllamaClient()

    # Simple generation
    response = client.generate("Summarize this document: ...")

    # Streaming generation
    for chunk in client.generate_stream("Analyze..."):
        print(chunk, end="", flush=True)

    # Entity extraction with structured prompts
    entities = client.extract_entities(document_text)

    # Memory management
    client.unload_model()  # Free GPU memory
"""

import gc
import json
from typing import Any, Dict, Generator, List, Optional

import requests
from requests.adapters import HTTPAdapter
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from urllib3.util.retry import Retry

from continuum_report.lib.config import settings
from continuum_report.lib.logging_config import get_logger

logger = get_logger(__name__)


class OllamaError(Exception):
    """Base exception for Ollama client errors."""
    pass


class OllamaConnectionError(OllamaError):
    """Failed to connect to Ollama server."""
    pass


class OllamaModelError(OllamaError):
    """Model not found or failed to load."""
    pass


class OllamaTimeoutError(OllamaError):
    """Request timed out."""
    pass


class OllamaClient:
    """
    Client for Ollama LLM API with retry logic and memory management.

    Designed for memory-constrained environments (16GB RAM).
    Includes automatic model unloading and garbage collection.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        context_size: Optional[int] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize Ollama client.

        Args:
            base_url: Ollama server URL (defaults to settings.ollama_url)
            model: Model name (defaults to settings.ollama_model)
            context_size: Context window size (defaults to settings.ollama_context_size)
            timeout: Request timeout in seconds (defaults to settings.ollama_timeout)
        """
        self.base_url = (base_url or settings.ollama_url).rstrip("/")
        self.model = model or settings.ollama_model
        self.context_size = context_size or settings.ollama_context_size
        self.timeout = timeout or settings.ollama_timeout

        # Create session with connection pooling
        self.session = self._create_session()

        # Track generation count for memory management
        self._generation_count = 0
        self._unload_every = settings.unload_model_every

        logger.debug(
            "Ollama client initialized",
            url=self.base_url,
            model=self.model,
            context_size=self.context_size
        )

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()

        # Retry strategy for transient failures
        retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    # =========================================================================
    # GENERATION
    # =========================================================================

    @retry(
        retry=retry_if_exception_type(OllamaConnectionError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: The user prompt
            system: Optional system prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response

        Raises:
            OllamaConnectionError: If connection fails
            OllamaModelError: If model fails to load
            OllamaTimeoutError: If request times out
        """
        logger.debug("Generating response", prompt_len=len(prompt))

        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": self.context_size,
                "temperature": temperature,
            }
        }

        if system:
            payload["system"] = system

        if max_tokens:
            payload["options"]["num_predict"] = max_tokens

        try:
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )

            if response.status_code == 404:
                raise OllamaModelError(f"Model '{self.model}' not found")
            elif response.status_code >= 400:
                raise OllamaError(f"API error {response.status_code}: {response.text}")

            result = response.json()
            generated_text = result.get("response", "")

            # Memory management
            self._generation_count += 1
            if self._generation_count >= self._unload_every:
                self.unload_model()
                self._generation_count = 0

            logger.debug(
                "Generation complete",
                response_len=len(generated_text),
                eval_count=result.get("eval_count"),
            )

            return generated_text

        except requests.exceptions.Timeout:
            logger.error("Request timed out", timeout=self.timeout)
            raise OllamaTimeoutError(f"Request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection failed", error=str(e))
            raise OllamaConnectionError(f"Cannot connect to {self.base_url}")
        except requests.exceptions.RequestException as e:
            logger.error("Request failed", error=str(e))
            raise OllamaError(f"Request failed: {e}")

    def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Generator[str, None, None]:
        """
        Generate a streaming response from the LLM.

        Args:
            prompt: The user prompt
            system: Optional system prompt
            temperature: Sampling temperature

        Yields:
            Text chunks as they are generated
        """
        logger.debug("Starting streaming generation", prompt_len=len(prompt))

        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "num_ctx": self.context_size,
                "temperature": temperature,
            }
        }

        if system:
            payload["system"] = system

        try:
            with self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                stream=True,
            ) as response:
                if response.status_code >= 400:
                    raise OllamaError(f"API error {response.status_code}")

                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            chunk = data.get("response", "")
                            if chunk:
                                yield chunk

                            # Check if done
                            if data.get("done"):
                                break
                        except json.JSONDecodeError:
                            continue

        except requests.exceptions.Timeout:
            raise OllamaTimeoutError(f"Stream timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            raise OllamaConnectionError(f"Cannot connect to {self.base_url}")

        # Memory management after streaming
        self._generation_count += 1
        if self._generation_count >= self._unload_every:
            self.unload_model()
            self._generation_count = 0

    # =========================================================================
    # SPECIALIZED PROMPTS
    # =========================================================================

    def extract_entities(
        self,
        text: str,
        entity_types: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Extract named entities from text.

        Args:
            text: Document text to analyze
            entity_types: Optional list of entity types to extract
                (default: Person, Organization, Location, Event)

        Returns:
            List of entity dictionaries with 'name', 'type', 'context'
        """
        if entity_types is None:
            entity_types = ["Person", "Organization", "Location", "Event", "Date"]

        system_prompt = """You are an entity extraction system. Extract named entities from the provided text.
Return ONLY a JSON array of entities. Each entity should have:
- name: The entity name as it appears in the text
- type: One of: Person, Organization, Location, Event, Date, Document
- context: A brief phrase showing how the entity appears in context

Return ONLY valid JSON. No explanations or other text."""

        prompt = f"""Extract all named entities from this text:

---
{text[:self.context_size * 2]}
---

Return entities as a JSON array. Types to extract: {', '.join(entity_types)}"""

        try:
            response = self.generate(prompt, system=system_prompt, temperature=0.1)

            # Parse JSON from response
            # Handle cases where model adds extra text
            json_start = response.find("[")
            json_end = response.rfind("]") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                logger.warning("No JSON array found in response")
                return []

        except json.JSONDecodeError as e:
            logger.warning("Failed to parse entity JSON", error=str(e))
            return []
        except OllamaError:
            raise

    def summarize(self, text: str, max_length: int = 200) -> str:
        """
        Generate a summary of the provided text.

        Args:
            text: Text to summarize
            max_length: Approximate maximum length of summary

        Returns:
            Summary text
        """
        system_prompt = "You are a concise summarization system. Provide clear, factual summaries."

        prompt = f"""Summarize the following text in approximately {max_length} words. Focus on key facts and findings.

---
{text[:self.context_size * 3]}
---

Summary:"""

        return self.generate(prompt, system=system_prompt, temperature=0.3)

    def analyze_connections(
        self,
        entity1: str,
        entity2: str,
        context: str,
    ) -> Dict[str, Any]:
        """
        Analyze the relationship between two entities.

        Args:
            entity1: First entity name
            entity2: Second entity name
            context: Document text providing context

        Returns:
            Dictionary with 'relationship', 'confidence', 'evidence'
        """
        system_prompt = """You analyze relationships between entities based on document evidence.
Return ONLY a JSON object with:
- relationship: Brief description of how entities are connected
- confidence: high, medium, or low
- evidence: Key quotes or facts supporting the connection"""

        prompt = f"""Analyze the relationship between "{entity1}" and "{entity2}" based on this text:

---
{context[:self.context_size * 2]}
---

Return ONLY valid JSON describing their relationship."""

        try:
            response = self.generate(prompt, system=system_prompt, temperature=0.2)

            # Parse JSON
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                return json.loads(response[json_start:json_end])
            else:
                return {
                    "relationship": "Unknown",
                    "confidence": "low",
                    "evidence": "Could not parse response"
                }

        except json.JSONDecodeError:
            return {
                "relationship": "Unknown",
                "confidence": "low",
                "evidence": "Failed to parse JSON response"
            }

    # =========================================================================
    # MEMORY MANAGEMENT
    # =========================================================================

    def unload_model(self) -> bool:
        """
        Unload the model from memory to free GPU/RAM.

        Returns:
            True if successful
        """
        logger.info("Unloading model to free memory", model=self.model)

        try:
            # Send a request with keep_alive=0 to unload
            self.session.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": "",
                    "keep_alive": 0,
                },
                timeout=30,
            )

            # Also trigger Python garbage collection
            gc.collect()

            logger.debug("Model unloaded successfully")
            return True

        except Exception as e:
            logger.warning("Failed to unload model", error=str(e))
            return False

    # =========================================================================
    # MODEL MANAGEMENT
    # =========================================================================

    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available models.

        Returns:
            List of model information dictionaries
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/tags",
                timeout=10,
            )
            response.raise_for_status()
            return response.json().get("models", [])
        except Exception as e:
            logger.error("Failed to list models", error=str(e))
            return []

    def model_exists(self, model_name: Optional[str] = None) -> bool:
        """
        Check if a model is available.

        Args:
            model_name: Model to check (defaults to configured model)

        Returns:
            True if model exists
        """
        model_name = model_name or self.model
        models = self.list_models()
        return any(m.get("name", "").startswith(model_name) for m in models)

    # =========================================================================
    # HEALTH CHECK
    # =========================================================================

    def health_check(self) -> bool:
        """
        Check if Ollama server is reachable.

        Returns:
            True if healthy
        """
        try:
            response = self.session.get(
                f"{self.base_url}/api/tags",
                timeout=5,
            )
            return response.status_code == 200
        except Exception:
            return False

    def close(self) -> None:
        """Close the session and optionally unload model."""
        self.unload_model()
        self.session.close()
        logger.debug("Ollama client closed")

    def __enter__(self) -> "OllamaClient":
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[Any]
    ) -> None:
        self.close()


# =============================================================================
# CLI UTILITY
# =============================================================================

def main() -> None:
    """Demo the client when run as a script."""
    print("=" * 60)
    print("The Continuum Report - Ollama Client Demo")
    print("=" * 60)
    print()

    client = OllamaClient()

    # Health check
    if client.health_check():
        print("Connection: OK")
        print(f"Server: {client.base_url}")
    else:
        print("Connection: FAILED")
        print("Is Ollama running?")
        return

    # List models
    models = client.list_models()
    print(f"Available models: {len(models)}")
    for model in models[:5]:
        print(f"  - {model.get('name')}")

    # Check configured model
    if client.model_exists():
        print(f"\nConfigured model '{client.model}': Available")
    else:
        print(f"\nConfigured model '{client.model}': NOT FOUND")
        print("Run: ollama pull mistral")
        return

    # Demo generation
    print("\n--- Demo Generation ---")
    print("Prompt: 'What is OSINT?'")
    print()

    try:
        response = client.generate(
            "What is OSINT? Answer in 2 sentences.",
            temperature=0.5,
        )
        print(f"Response: {response}")
    except OllamaError as e:
        print(f"Error: {e}")

    # Cleanup
    print("\n--- Cleanup ---")
    client.unload_model()
    print("Model unloaded.")


if __name__ == "__main__":
    main()
