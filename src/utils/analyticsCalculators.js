/**
 * Pure functions for computing analytics from the gig data array.
 * All functions are stateless and side-effect free.
 */

export function buildArtistLeaderboard(gigs) {
  const map = {}
  for (const gig of gigs) {
    const artists = [...new Set([...(gig.headliners ?? []), ...(gig.artists_seen ?? [])])]
    for (const artist of artists) {
      if (!artist) continue
      if (!map[artist]) {
        map[artist] = { artist, gigsCount: 0 }
      }
      map[artist].gigsCount += 1
    }
  }
  return Object.values(map).sort((a, b) => b.gigsCount - a.gigsCount)
}
