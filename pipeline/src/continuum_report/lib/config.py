"""
The Continuum Report - Centralized Configuration

Uses Pydantic Settings for type-safe configuration with environment variable loading.
Secrets are loaded from environment variables (never hardcoded).

Usage:
    from continuum_report.lib.config import settings

    # Access configuration
    print(settings.paperless_url)
    print(settings.ollama_model)

    # Access paths
    print(settings.reports_dir)

Environment Variables (set in .env file or system environment):
    PAPERLESS_URL       - Paperless-ngx server URL
    PAPERLESS_TOKEN     - API authentication token (REQUIRED, SENSITIVE)
    OLLAMA_URL          - Ollama server URL
    OLLAMA_MODEL        - LLM model name (default: mistral)
    CONTINUUM_BASE_DIR  - Base directory for all data (default: /continuum)
"""

from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ContinuumSettings(BaseSettings):
    """
    Centralized configuration for The Continuum Report pipeline.

    All sensitive values are loaded from environment variables.
    Paths are automatically created if they don't exist.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # =========================================================================
    # PAPERLESS-NGX CONFIGURATION
    # =========================================================================

    paperless_url: str = Field(
        default="http://localhost:8040",
        description="Paperless-ngx server URL (WoodsDen local)"
    )

    paperless_token: str = Field(
        default="",
        description="Paperless-ngx API token (REQUIRED)"
    )

    paperless_timeout: int = Field(
        default=30,
        description="API request timeout in seconds"
    )

    # =========================================================================
    # OLLAMA CONFIGURATION
    # =========================================================================

    ollama_url: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL (WoodsDen local)"
    )

    ollama_model: str = Field(
        default="mistral",
        description="LLM model to use for processing"
    )

    ollama_context_size: int = Field(
        default=1024,
        description="Context window size (lower = less RAM)"
    )

    ollama_timeout: int = Field(
        default=600,
        description="LLM request timeout in seconds (10 minutes default)"
    )

    # =========================================================================
    # DIRECTORY CONFIGURATION
    # =========================================================================

    continuum_base_dir: Path = Field(
        default=Path("C:/Users/Xx LilMan xX/Documents/Claude Docs/Continuum"),
        description="Base directory for all Continuum data (WoodsDen local)"
    )

    @property
    def data_dir(self) -> Path:
        """Directory for entity data and checkpoints."""
        return self.continuum_base_dir / "entity_data"

    @property
    def reports_dir(self) -> Path:
        """Directory for generated reports and dossiers."""
        return self.continuum_base_dir / "reports"

    @property
    def checkpoint_dir(self) -> Path:
        """Directory for processing checkpoints."""
        return self.continuum_base_dir / "checkpoints"

    @property
    def documents_inbox(self) -> Path:
        """Directory for document inbox."""
        return self.continuum_base_dir / "documents" / "inbox"

    @property
    def entity_db_file(self) -> Path:
        """Path to the entity database JSON file."""
        return self.data_dir / "entity_database.json"

    @property
    def dossier_queue_file(self) -> Path:
        """Path to the dossier queue JSON file."""
        return self.data_dir / "dossier_queue.json"

    # =========================================================================
    # WEBSITE CONFIGURATION
    # =========================================================================

    website_base_url: str = Field(
        default="https://thecontinuumreport.com",
        description="Base URL for the public website"
    )

    # =========================================================================
    # PROCESSING CONFIGURATION
    # =========================================================================

    max_documents_to_search: int = Field(
        default=9999,
        description="Maximum documents to search (no artificial cap)"
    )

    max_documents_for_entities: int = Field(
        default=9999,
        description="Maximum documents for entity extraction"
    )

    max_documents_for_dossier: int = Field(
        default=9999,
        description="Maximum documents for dossier generation"
    )

    max_chunk_size: int = Field(
        default=1500,
        description="Characters per text chunk (reduced for memory)"
    )

    # =========================================================================
    # MEMORY SAFETY SETTINGS (for 16GB RAM systems)
    # =========================================================================

    delay_between_docs: int = Field(
        default=10,
        description="Seconds to wait between processing documents"
    )

    delay_between_batches: int = Field(
        default=30,
        description="Seconds to wait every 5 documents"
    )

    unload_model_every: int = Field(
        default=10,
        description="Unload Ollama model every N docs to clear memory"
    )

    # =========================================================================
    # VALIDATION
    # =========================================================================

    @field_validator("paperless_token")
    @classmethod
    def validate_paperless_token(cls, v: str) -> str:
        """Warn if Paperless token is not configured."""
        if not v:
            import warnings
            warnings.warn(
                "PAPERLESS_TOKEN is not set. Set it in your .env file or environment.",
                UserWarning,
                stacklevel=2
            )
        return v

    @field_validator("continuum_base_dir", mode="before")
    @classmethod
    def parse_path(cls, v: str | Path) -> Path:
        """Convert string paths to Path objects."""
        if isinstance(v, str):
            return Path(v)
        return v

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def ensure_directories(self) -> None:
        """Create all required directories if they don't exist."""
        dirs = [
            self.data_dir,
            self.reports_dir,
            self.checkpoint_dir,
            self.documents_inbox,
        ]
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)

    def validate_connection(self) -> dict:
        """
        Validate connections to external services.

        Returns:
            dict: Status of each service connection
        """
        import requests

        status = {
            "paperless": False,
            "ollama": False,
            "errors": []
        }

        # Check Paperless
        try:
            resp = requests.get(
                f"{self.paperless_url}/api/",
                headers={"Authorization": f"Token {self.paperless_token}"},
                timeout=5
            )
            status["paperless"] = resp.status_code == 200
            if not status["paperless"]:
                status["errors"].append(f"Paperless returned {resp.status_code}")
        except Exception as e:
            status["errors"].append(f"Paperless connection failed: {e}")

        # Check Ollama
        try:
            resp = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            status["ollama"] = resp.status_code == 200
            if not status["ollama"]:
                status["errors"].append(f"Ollama returned {resp.status_code}")
        except Exception as e:
            status["errors"].append(f"Ollama connection failed: {e}")

        return status

    def __repr__(self) -> str:
        """Safe representation that doesn't expose secrets."""
        return (
            f"ContinuumSettings("
            f"paperless_url={self.paperless_url!r}, "
            f"ollama_url={self.ollama_url!r}, "
            f"ollama_model={self.ollama_model!r}, "
            f"base_dir={self.continuum_base_dir!r})"
        )


# Singleton instance - import this in other modules
settings = ContinuumSettings()


# =============================================================================
# CLI UTILITY
# =============================================================================

def main() -> None:
    """Quick validation when run as a script."""
    print("=" * 60)
    print("The Continuum Report - Configuration Check")
    print("=" * 60)
    print()
    print(f"Configuration: {settings}")
    print()
    print("Directories:")
    print(f"  Base:       {settings.continuum_base_dir}")
    print(f"  Data:       {settings.data_dir}")
    print(f"  Reports:    {settings.reports_dir}")
    print(f"  Checkpoints:{settings.checkpoint_dir}")
    print()
    print("Services:")
    print(f"  Paperless:  {settings.paperless_url}")
    print(f"  Ollama:     {settings.ollama_url} (model: {settings.ollama_model})")
    print()

    # Check if token is set
    if settings.paperless_token:
        print("  Token:      [SET]")
    else:
        print("  Token:      [NOT SET - check .env file]")
    print()

    # Validate connections
    print("Validating connections...")
    status = settings.validate_connection()
    print(f"  Paperless:  {'OK' if status['paperless'] else 'FAILED'}")
    print(f"  Ollama:     {'OK' if status['ollama'] else 'FAILED'}")

    if status["errors"]:
        print()
        print("Errors:")
        for err in status["errors"]:
            print(f"  - {err}")


if __name__ == "__main__":
    main()
