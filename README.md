# Gig-ography

A personal, public-facing static website that archives a lifetime of concerts and festivals.

**Live site:** `https://defaultbob.github.io/gig-ography/`

---

## What it does

- **Archive grid** — Every gig as a card with image, date, venue, headliners, and support acts.
- **Festival cards** — Multi-day events show a full lineup with "Who I Saw" highlights.
- **Analytics dashboard** — Artist leaderboard.

---

## Quick start

```bash
npm install && npm run dev
```

Opens at `http://localhost:5173/`.

---

## Project structure

```
gig-ography/
├── data/
│   └── gigs.yaml               # Canonical archive — what the frontend renders
├── src/                        # React frontend
├── .github/workflows/          # GitHub Actions deployment
└── vite.config.js
```

---

## Adding gigs

Open [data/gigs.yaml](data/gigs.yaml) and add an entry:

```yaml
- headliners:
    - "Artist Name"             # required — use multiple entries for co-headliners
  support:
    - "Support Act"             # optional
  date: 2024-06-15              # YYYY-MM-DD — start date
  venue: "Venue Name"
  city: "City"
  image_url: "https://..."      # optional
```

### Multi-day events (festivals)

Set `end_date` to a different date — the card automatically shows the date range and a "festival" badge. Add `lineup` and `artists_seen` to show the full lineup with seen-artist highlights:

```yaml
- headliners:
    - "Headliner 1"
    - "Headliner 2"
  date: 2024-08-23              # start date
  end_date: 2024-08-25          # end date — triggers festival display
  venue: "Festival Site"
  city: "City"
  lineup:
    - "Headliner 1"
    - "Headliner 2"
    - "Everyone Else"           # full lineup shown on the card
  artists_seen:
    - "Headliner 1"             # highlighted in the lineup display
```

Push to `main` and the site redeploys automatically.

---

## Deployment

The site deploys automatically to GitHub Pages on every push to `main` via GitHub Actions.

### First-time setup

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source** and select **GitHub Actions**
3. Push any commit to `main` — the workflow builds and deploys the site

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 6, Tailwind CSS v4 |
| Data | YAML (bundled at build time — no backend) |
| Hosting | GitHub Pages |
| CI/CD | GitHub Actions |
