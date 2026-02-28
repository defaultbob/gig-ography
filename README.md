# Gig-ography

A personal, public-facing static website that archives a lifetime of concerts and festivals. Includes an analytics dashboard and an automated data enrichment pipeline.

**Live site:** `https://defaultbob.github.io/gig-ography/`

---

## What it does

- **Archive grid** — Every gig and festival as a card with image, date, venue, and streaming links
- **Festival mode** — Lineup poster with "Who I Saw" artist highlights
- **Analytics dashboard** — Artist leaderboard, most-heard songs, and top venues
- **Solicitor CLI** — Local Python tool that parses Gmail data (via Gemini), merges manual entries, and enriches everything with setlist data, artist images, and streaming links

---

## Project structure

```
gig-ography/
├── data/
│   ├── master_gigs.yaml        # The canonical gig archive — edit this to add gigs
│   └── manual_entries.yaml     # Gigs not in email — input for the Solicitor tool
├── src/                        # React frontend
├── solicitor/                  # Python enrichment CLI
├── .github/workflows/          # GitHub Actions deployment
└── vite.config.js
```

---

## Frontend

### Prerequisites

- Node.js 18+
- npm

### Install

```bash
npm install
```

### Local development

```bash
npm run dev
```

Opens at `http://localhost:5173/gig-ography/`.

### Production build

```bash
npm run build
```

Output goes to `dist/`. Preview it locally with:

```bash
npm run preview
```

---

## Adding gigs

Open [data/master_gigs.yaml](data/master_gigs.yaml) and add an entry following this schema:

```yaml
- artist: "Artist Name"
  date: 2024-06-15          # YYYY-MM-DD
  venue: "Venue Name"
  city: "City"
  type: "gig"               # "gig" or "festival"
  setlist_url: "https://www.setlist.fm/..."
  total_songs: 20
  top_songs: ["Song A", "Song B", "Song C"]
  image_url: "https://..."
  streaming:
    spotify: "https://open.spotify.com/artist/..."
    apple: "https://music.apple.com/..."
```

For festivals, add these extra fields:

```yaml
  festival_artists: ["Artist A", "Artist B", "Artist C"]  # full lineup
  artists_seen: ["Artist A"]                               # who you actually saw
```

Push to `main` and the site redeploys automatically.

---

## Solicitor — automated enrichment

The Solicitor is a local CLI tool that automates data collection from Gmail and enriches it with setlist data, artist images, and streaming links. It writes a `proposed_changes.yaml` for you to review before anything touches `master_gigs.yaml`.

### Prerequisites

- Python 3.11+

### Install

```bash
cd solicitor
pip install -r requirements.txt
```

### Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

| Key | Where to get it |
|-----|----------------|
| `SETLIST_FM_API_KEY` | [api.setlist.fm](https://api.setlist.fm) — free registration |
| `SPOTIPY_CLIENT_ID` / `SPOTIPY_CLIENT_SECRET` | [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) — free |
| `APPLE_MUSIC_*` | Apple Developer Program ($99/yr) — optional, enrichment skips gracefully if absent |
| `MUSICBRAINZ_APP_EMAIL` | Any valid email — required by MusicBrainz ToS for the User-Agent string |

### Usage

**Step 1** — Export your concert emails from Gmail using the Gemini Gmail Extension, copy the output to a `.txt` file.

**Step 2** — Optionally add any gigs not found in email to `data/manual_entries.yaml`.

**Step 3** — Run the Solicitor:

```bash
cd solicitor
python solicitor.py ../my_gmail_export.txt
```

Options:

```
python solicitor.py <gemini_txt> [--manual <path>] [--output <path>] [--skip-enrichment]

  --manual            Path to manual_entries.yaml (default: ../data/manual_entries.yaml)
  --output            Output path (default: ../data/proposed_changes.yaml)
  --skip-enrichment   Merge only, skip API calls (useful for testing)
```

**Step 4** — Review `data/proposed_changes.yaml`, edit as needed, then copy approved entries into `data/master_gigs.yaml`.

### What the Solicitor enriches

| Field | Source |
|-------|--------|
| `setlist_url`, `total_songs`, `top_songs` | Setlist.fm (exact match, or tour average if no match) |
| `image_url` | MusicBrainz → Wikipedia → Wikimedia Commons |
| `streaming.spotify` | Spotify API |
| `streaming.apple` | Apple Music API |

Enrichment never overwrites fields that are already populated — it only fills in gaps.

---

## Deployment

The site deploys automatically to GitHub Pages on every push to `main` via GitHub Actions.

### First-time setup

1. Push this repo to GitHub under `defaultbob/gig-ography`
2. Go to **Settings → Pages → Source** and select **GitHub Actions**
3. Push any commit to `main` — the workflow builds and deploys the site

The live URL will be: `https://defaultbob.github.io/gig-ography/`

### How it works

`.github/workflows/deploy.yml` runs `npm ci && npm run build` on every push to `main`, then uploads `dist/` as a GitHub Pages artifact.

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 6, Tailwind CSS v4 |
| Data | YAML (bundled at build time — no backend) |
| Enrichment CLI | Python 3.11, spotipy, musicbrainzngs, setlist-fm-client |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
