"""
Parses raw text copy-pasted from the Gemini Gmail Extension.

Expected format: a free-form text block where each gig appears as a chunk
with lines containing an artist name, a date, and a venue/location.
The parser uses heuristics + dateutil to extract structured entries.

Usage:
    from parser import parse_gemini_txt
    gigs = parse_gemini_txt("path/to/gemini_export.txt")
"""

import re
from dateutil import parser as dateparser
from dateutil.parser import ParserError


def parse_gemini_txt(filepath: str) -> list[dict]:
    """Return a list of partial gig dicts extracted from a Gemini .txt file."""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    blocks = _split_into_blocks(text)
    gigs = []
    for block in blocks:
        gig = _parse_block(block)
        if gig:
            gigs.append(gig)
    return gigs


def _split_into_blocks(text: str) -> list[str]:
    """Split the raw text into per-gig blocks on blank lines."""
    # Split on two or more consecutive newlines
    return [b.strip() for b in re.split(r"\n{2,}", text) if b.strip()]


def _parse_block(block: str) -> dict | None:
    """
    Try to extract artist, date, venue, and city from a text block.
    Returns None if no date can be reliably found.
    """
    lines = [l.strip() for l in block.splitlines() if l.strip()]
    if not lines:
        return None

    date_str = None
    date_line_idx = None
    for i, line in enumerate(lines):
        parsed = _try_parse_date(line)
        if parsed:
            date_str = parsed
            date_line_idx = i
            break

    if not date_str:
        return None

    # Heuristic: artist is the first line (or line before the date line)
    artist = lines[0] if date_line_idx != 0 else None

    # Venue / city: lines after the date line
    venue_lines = [l for l in lines[date_line_idx + 1:] if l] if date_line_idx is not None else []
    venue = venue_lines[0] if venue_lines else None
    city = venue_lines[1] if len(venue_lines) > 1 else None

    if not artist:
        return None

    return {
        "artist": artist,
        "date": date_str,
        "venue": venue or "",
        "city": city or "",
        "type": "gig",
        "setlist_url": None,
        "total_songs": None,
        "top_songs": [],
        "image_url": None,
        "streaming": {"spotify": None, "apple": None},
    }


def _try_parse_date(text: str) -> str | None:
    """
    Attempt to parse a date from a string.
    Returns ISO format YYYY-MM-DD on success, None on failure.
    """
    # Strip common noise words before trying
    cleaned = re.sub(r"\b(on|at|the|concert|show|gig|festival)\b", "", text, flags=re.IGNORECASE)
    try:
        dt = dateparser.parse(cleaned, dayfirst=True, fuzzy=True)
        if dt and 1980 <= dt.year <= 2040:
            return dt.strftime("%Y-%m-%d")
    except (ParserError, OverflowError, ValueError):
        pass
    return None
