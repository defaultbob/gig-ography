#!/usr/bin/env python3
"""
Solicitor — Gig data pipeline CLI.

Workflow:
  1. Parse raw Gemini Gmail Extension .txt export
  2. Merge with manual_entries.yaml (email wins on date conflicts)
  3. Enrich each gig via Setlist.fm, MusicBrainz, Spotify, Apple Music
  4. Write proposed_changes.yaml for manual review

Usage:
  cd solicitor/
  python solicitor.py ../gemini_export.txt
  python solicitor.py ../gemini_export.txt --manual ../data/manual_entries.yaml
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the solicitor directory (or parent)
load_dotenv(Path(__file__).parent / ".env")
load_dotenv(Path(__file__).parent.parent / ".env")

from parser import parse_gemini_txt
from merger import merge_sources
from enricher import enrich_gigs
from output import write_proposed_changes


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Solicitor: enrich gig data from Gemini Gmail export."
    )
    ap.add_argument("gemini_txt", help="Path to the Gemini Gmail Extension .txt export")
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

    print(f"Step 1/3  Parsing {args.gemini_txt}")
    email_gigs = parse_gemini_txt(args.gemini_txt)
    print(f"  → Found {len(email_gigs)} gig(s) in email export.")

    print(f"\nStep 2/3  Merging with {args.manual}")
    merged = merge_sources(email_gigs, args.manual)
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
