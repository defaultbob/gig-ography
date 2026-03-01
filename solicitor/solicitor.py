#!/usr/bin/env python3
"""
Solicitor — Gig data pipeline CLI.

Workflow:
  1. Reads gigs from a YAML file (e.g., google_gigs.yaml)
  2. Merge with manual_entries.yaml (input YAML wins on date conflicts)
  3. Enrich each gig via Setlist.fm, MusicBrainz, Spotify, Apple Music
  4. Write proposed_changes.yaml for manual review

Usage:
  cd solicitor/
  python solicitor.py
  python solicitor.py --input-yaml ../data/google_gigs.yaml --manual ../data/manual_entries.yaml
"""

import argparse
import sys
from pathlib import Path
import yaml

from dotenv import load_dotenv

# Load .env from the solicitor directory (or parent)
load_dotenv(Path(__file__).parent / ".env")
load_dotenv(Path(__file__).parent.parent / ".env")

from parser import parse_plaintext_gigs
from merger import merge_sources
from enricher import enrich_gigs
from output import write_proposed_changes
 

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Solicitor: enrich gig data from a YAML input file."
    )
    ap.add_argument(
        "--input-yaml",
        dest="input_file", # Renamed for clarity
        default=str(Path(__file__).parent.parent / "data" / "plaintext guesses.md"), # Changed default to plaintext
        help="Path to the input YAML file (default: ../data/google_gigs.yaml)",
    )
    ap.add_argument(
        "--manual",
        default=str(Path(__file__).parent.parent / "data" / "manual_entries.yaml"),
        help="Path to manual_entries.yaml (default: ../data/manual_entries.yaml)",
    )
    ap.add_argument(
        "--output",
        default=str(Path(__file__).parent.parent / "data" / "proposed_changes.yaml"),
        help="Output path for proposed_changes.yaml (default: ../data/proposed_changes.yaml)",
    )
    ap.add_argument(
        "--skip-enrichment",
        action="store_true",
        help="Merge only — skip API enrichment (useful for testing the parser/merger)",
    )
    args = ap.parse_args()

    print("Solicitor starting…\n")

    print(f"Step 1/3  Parsing {args.input_file}")
    try:
        with open(args.input_file, encoding="utf-8") as f:
            content = f.read()
        input_gigs = parse_plaintext_gigs(content)
    except FileNotFoundError:
        print(f"  → Input file not found: {args.input_file}. Starting with an empty list.")
        input_gigs = []
    print(f"  → Found {len(input_gigs)} gig(s) in {args.input_yaml}.")

    print(f"\nStep 2/3  Merging with {args.manual}")
    # Note: The merge_sources function expects the first argument to be the "primary" source.
    # In the old script, this was email_gigs. Now it's the input_gigs.
    merged = merge_sources(input_gigs, args.manual)
    print(f"  → {len(merged)} gig(s) after merge.")

    if args.skip_enrichment:
        print("\nStep 3/3  Skipping enrichment (--skip-enrichment flag set).")
        enriched = merged
    else:
        print(f"\nStep 3/3  Enriching {len(merged)} gig(s) via APIs…")
        enriched = enrich_gigs(merged)

    write_proposed_changes(enriched, args.output)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
