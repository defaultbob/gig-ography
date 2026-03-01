"""Writes the proposed changes to a YAML file for user review."""

import yaml
from typing import Dict, List


def write_proposed_changes(gigs: List[Dict], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f: #
        yaml.dump(gigs, f, default_flow_style=False, allow_unicode=True, sort_keys=False) #
    print(f"\nProposed changes written to: {output_path}")
    print("Review and edit this file, then copy approved entries into data/master_gigs.yaml.")
