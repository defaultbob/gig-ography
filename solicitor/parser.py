"""Parses the plaintext output from the Gemini Gmail Extension."""

import logging
import re
from typing import Dict, List
from dateutil.parser import parse


def parse_plaintext_gigs(content: str) -> List[Dict]:
    """
    Parse plaintext content into a list of gig dictionaries.
    Expected format per entry:
    - `* ARTIST, [VENUE, [CITY]], [DATE]` (in any order)
    """
    gigs = []
    # Regex to find a year or date-like pattern. This is intentionally broad.
    # It looks for 4-digit years, year ranges, or common date formats.
    date_pattern = re.compile(
        r"((?:circa|c\.|around)\s*)?(\b\d{4}\b(-\d{2,4})?|\b(?:[A-Za-z]{3,9})\s\d{1,2},?\s\d{4})"
        r"((?:circa|c\.|around)\s*)?"  # Optional "circa" prefix
        r"("
        r"\b\d{4}\b(?:-\d{2,4})?"  # YYYY or YYYY-YY/YYYY
        r"|"
        r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}(?:\s+(?:[01]?\d|2[0-3]):[0-5]\d(?:[ap]m)?)?"  # Month Day, Year (with optional time)
        r"|"
        r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}(?:\s+(?:[01]?\d|2[0-3]):[0-5]\d(?:[ap]m)?)?"  # Day Month Year (with optional time)
        r"|"
        r"\b\d{4}-\d{2}-\d{2}\b" # YYYY-MM-DD
        r"|"
        r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}(?:\s+(?:[01]?\d|2[0-3]):[0-5]\d(?:[ap]m)?)?" # DayOfWeek, Month Day, Year
        r")"
    )

    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("* ") or len(line) < 5:
            continue

        line_content = line[2:].strip()
        match = date_pattern.search(line_content)

        if not match:
            logging.warning(f"Could not find a date in line, skipping: {line!r}")
            continue

        date_str = match.group(0)
        # Use fuzzy parsing for the date part. It will pick the first year it finds.
        parsed_date = parse(date_str, fuzzy=True).strftime("%Y-%m-%d")

        # Remove the date string and any surrounding commas/spaces to isolate other parts
        remaining_str = line_content.replace(date_str, "").strip(" ,")
        parts = [p.strip() for p in remaining_str.split(",") if p.strip()]

        if not parts:
            logging.warning(f"Could not find artist/venue in line, skipping: {line!r}")
            continue

        # Assume the first part is always the artist
        artist = parts.pop(0)
        venue = ""
        city = ""

        if len(parts) > 1: # We likely have venue and city
            venue = parts[0]
            city = parts[1]
        elif len(parts) == 1: # Assume it's the venue
            venue = parts[0]

        gigs.append({"artist": artist, "date": parsed_date, "venue": venue, "city": city})

    return gigs