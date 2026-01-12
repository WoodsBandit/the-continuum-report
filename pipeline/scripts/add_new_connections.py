#!/usr/bin/env python3
"""
add_new_connections.py - Add new connections for created briefs to connections.json
"""

import json
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(r"T:")
CONNECTIONS_JSON = PROJECT_ROOT / "website" / "data" / "connections.json"
BACKLOG_JSON = PROJECT_ROOT / "website" / "data" / "connections_backlog.json"
CONNECTIONS_DIR = PROJECT_ROOT / "website" / "briefs" / "connections"

# New connections that were created (with their brief files)
NEW_CONNECTIONS = [
    # NXIVM connections
    {"source": "clare-bronfman", "target": "keith-raniere", "type": "referenced", "evidence": ["Court records"], "brief_file": "clare-bronfman_keith-raniere.md", "summary": "Clare Bronfman's financial backing of Keith Raniere and NXIVM documented in federal court proceedings."},
    {"source": "clare-bronfman", "target": "nxivm-case", "type": "referenced", "evidence": ["Court records"], "brief_file": "clare-bronfman_nxivm-case.md", "summary": "Clare Bronfman as defendant in NXIVM federal prosecution, sentenced to 81 months."},
    {"source": "allison-mack", "target": "keith-raniere", "type": "referenced", "evidence": ["Court records"], "brief_file": "allison-mack_keith-raniere.md", "summary": "Allison Mack's role as DOS first-line master under Keith Raniere documented in federal prosecution."},
    {"source": "allison-mack", "target": "nxivm-case", "type": "referenced", "evidence": ["Court records"], "brief_file": "allison-mack_nxivm-case.md", "summary": "Allison Mack as defendant in NXIVM case, pleaded guilty to racketeering, sentenced to 3 years."},
    {"source": "allison-mack", "target": "clare-bronfman", "type": "referenced", "evidence": ["Court records"], "brief_file": "allison-mack_clare-bronfman.md", "summary": "Co-defendants in NXIVM federal prosecution with differing sentences reflecting cooperation levels."},
    {"source": "keith-raniere", "target": "nxivm-case", "type": "referenced", "evidence": ["Federal court records"], "brief_file": "keith-raniere_nxivm-case.md", "summary": "Keith Raniere as primary defendant, convicted on all counts, sentenced to 120 years."},

    # Iran-Contra connections
    {"source": "iran-contra-case", "target": "intelligence-financial-nexus", "type": "referenced", "evidence": ["Congressional Report"], "brief_file": "iran-contra-case_intelligence-financial-nexus.md", "summary": "Iran-Contra as foundational example of intelligence-financial nexus with 'The Enterprise' private network."},
    {"source": "iran-contra-case", "target": "promis-inslaw-case", "type": "referenced", "evidence": ["Secondary analysis"], "brief_file": "iran-contra-case_promis-inslaw-case.md", "summary": "Parallel scandals during Reagan administration with temporal and institutional overlap."},
    {"source": "iran-contra-case", "target": "bcci", "type": "referenced", "evidence": ["Secondary analysis"], "brief_file": "bcci_iran-contra-case.md", "summary": "BCCI facilitated financial transactions connected to Iran-Contra operations per Kerry Committee."},

    # Oliver North connections
    {"source": "oliver-north", "target": "iran-contra-case", "type": "documented", "evidence": ["Congressional Report"], "brief_file": "oliver-north_iran-contra-case.md", "summary": "Oliver North as central operative coordinating Iran-Contra covert operations from NSC staff."},
    {"source": "oliver-north", "target": "william-casey", "type": "documented", "evidence": ["Congressional Report"], "brief_file": "oliver-north_william-casey.md", "summary": "Casey-North relationship as strategic-operational axis of Iran-Contra enterprise."},

    # William Casey connections
    {"source": "william-casey", "target": "iran-contra-case", "type": "documented", "evidence": ["Congressional Report"], "brief_file": "william-casey_iran-contra-case.md", "summary": "CIA Director Casey's central role in Iran-Contra operations per congressional investigation."},
    {"source": "william-casey", "target": "oliver-north", "type": "referenced", "evidence": ["Congressional Report"], "brief_file": "william-casey_oliver-north.md", "summary": "Casey provided direction to North on covert operations including recruitment of Secord."},
    {"source": "william-casey", "target": "bcci", "type": "referenced", "evidence": ["Senate BCCI Report"], "brief_file": "william-casey_bcci.md", "summary": "CIA-BCCI banking relationships documented during Casey's tenure per Kerry Committee."},
    {"source": "william-casey", "target": "intelligence-financial-nexus", "type": "documented", "evidence": ["Appointment record"], "brief_file": "william-casey_intelligence-financial-nexus.md", "summary": "Casey's Wall Street background shaped sophisticated financial architecture for covert operations."},

    # Mossad connections
    {"source": "mossad", "target": "robert-maxwell", "type": "referenced", "evidence": ["Published accounts"], "brief_file": "mossad_robert-maxwell.md", "summary": "Alleged Mossad connection to Robert Maxwell examined in congressional investigation and published accounts."},
    {"source": "mossad", "target": "promis-inslaw-case", "type": "referenced", "evidence": ["Congressional testimony"], "brief_file": "mossad_promis-inslaw-case.md", "summary": "Allegations of Mossad involvement in PROMIS distribution examined by House Judiciary Committee."},
    {"source": "mossad", "target": "intelligence-financial-nexus", "type": "referenced", "evidence": ["General knowledge"], "brief_file": "mossad_intelligence-financial-nexus.md", "summary": "Alleged intersection of Mossad operations with financial networks per congressional testimony."},

    # BCCI connections
    {"source": "bcci", "target": "intelligence-financial-nexus", "type": "referenced", "evidence": ["Senate Report"], "brief_file": "bcci_intelligence-financial-nexus.md", "summary": "BCCI exemplifies intelligence-financial nexus with documented multi-service relationships."},
    {"source": "bcci", "target": "promis-inslaw-case", "type": "referenced", "evidence": ["Secondary analysis"], "brief_file": "bcci_promis-inslaw-case.md", "summary": "Parallel 1992 congressional investigations examining intelligence community connections."},

    # CIA connections
    {"source": "cia", "target": "bcci", "type": "referenced", "evidence": ["Senate Report (1992)"], "brief_file": "cia_bcci.md", "summary": "CIA utilized BCCI while possessing knowledge of criminal activities per Senate investigation."},
    {"source": "cia", "target": "iran-contra-case", "type": "referenced", "evidence": ["Congressional Report (1987)"], "brief_file": "cia_iran-contra-case.md", "summary": "CIA Director Casey played central role in Iran-Contra operations per congressional report."},
    {"source": "cia", "target": "promis-inslaw-case", "type": "referenced", "evidence": ["Congressional testimony"], "brief_file": "cia_promis-inslaw-case.md", "summary": "Allegations of CIA involvement in PROMIS distribution examined but not definitively resolved."},
    {"source": "cia", "target": "mossad", "type": "referenced", "evidence": ["Multiple sources"], "brief_file": "cia_mossad.md", "summary": "Publicly acknowledged intelligence partnership subject to congressional oversight."},

    # PROMIS connections
    {"source": "promis-inslaw-case", "target": "robert-maxwell", "type": "referenced", "evidence": ["Secondary sources"], "brief_file": "promis-inslaw-case_robert-maxwell.md", "summary": "Alleged Robert Maxwell role in PROMIS distribution examined in congressional testimony."},
    {"source": "promis-inslaw-case", "target": "intelligence-financial-nexus", "type": "referenced", "evidence": ["Congressional testimony"], "brief_file": "promis-inslaw-case_intelligence-financial-nexus.md", "summary": "PROMIS case illustrates intelligence-financial interface with private intermediaries."},
    {"source": "promis-inslaw-case", "target": "ghislaine-maxwell", "type": "referenced", "evidence": ["Inference"], "brief_file": "promis-inslaw-case_ghislaine-maxwell.md", "summary": "Indirect familial connection through Robert Maxwell; Ghislaine not in PROMIS documentation."},

    # Roy Cohn connections
    {"source": "roy-cohn", "target": "donald-trump", "type": "referenced", "evidence": ["Documented"], "brief_file": "roy-cohn_donald-trump.md", "summary": "Mentor-protege and attorney-client relationship from 1973-1986 shaping Trump's tactics."},
    {"source": "roy-cohn", "target": "meyer-lansky", "type": "referenced", "evidence": ["Secondary sources"], "brief_file": "roy-cohn_meyer-lansky.md", "summary": "Overlapping social-criminal networks in mid-20th century New York."},
    {"source": "roy-cohn", "target": "jeffrey-epstein", "type": "referenced", "evidence": ["Analytical inference"], "brief_file": "roy-cohn_jeffrey-epstein.md", "summary": "Indirect theoretical network connection through Trump; temporal gap makes direct contact implausible."},

    # Meyer Lansky connections
    {"source": "meyer-lansky", "target": "roy-cohn", "type": "referenced", "evidence": ["Secondary sources"], "brief_file": "meyer-lansky_roy-cohn.md", "summary": "Both operated in overlapping NYC social and criminal networks from 1950s-1980s."},
]

def main():
    # Load current connections
    with open(CONNECTIONS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing_pairs = {(c['source'], c['target']) for c in data['connections']}

    # Add new connections
    added = 0
    for conn in NEW_CONNECTIONS:
        pair = (conn['source'], conn['target'])
        reverse_pair = (conn['target'], conn['source'])

        # Check if brief file exists
        brief_path = CONNECTIONS_DIR / conn['brief_file']
        if not brief_path.exists():
            # Try the reverse naming
            reverse_file = f"{conn['target']}_{conn['source']}.md"
            reverse_path = CONNECTIONS_DIR / reverse_file
            if reverse_path.exists():
                conn['brief_file'] = reverse_file
            else:
                print(f"  SKIP: Brief not found: {conn['brief_file']}")
                continue

        # Skip if already exists
        if pair in existing_pairs or reverse_pair in existing_pairs:
            print(f"  EXISTS: {conn['source']} <-> {conn['target']}")
            continue

        # Add connection
        new_conn = {
            "source": conn['source'],
            "target": conn['target'],
            "strength": 50,
            "type": conn.get('type', 'referenced'),
            "evidence": conn.get('evidence', []),
            "bidirectional": True,
            "source_mentions_target": True,
            "target_mentions_source": True,
            "summary": conn.get('summary', f"Connection documented in analytical briefs."),
            "brief_file": conn['brief_file']
        }
        data['connections'].append(new_conn)
        existing_pairs.add(pair)
        added += 1
        print(f"  ADDED: {conn['source']} <-> {conn['target']}")

    # Update metadata
    data['generated'] = datetime.now(timezone.utc).isoformat()
    data['count'] = len(data['connections'])
    data['source'] = 'updated with new connection briefs'

    # Write updated file
    with open(CONNECTIONS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"Added {added} new connections")
    print(f"Total connections: {data['count']}")
    print(f"Saved to: {CONNECTIONS_JSON}")

if __name__ == '__main__':
    main()
