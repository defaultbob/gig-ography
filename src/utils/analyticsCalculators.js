/**
 * Pure functions for computing analytics from the gig data array.
 * All functions are stateless and side-effect free.
 */

export function buildArtistLeaderboard(gigs) {
  const map = {}
  for (const gig of gigs) {
    const key = gig.artist
    if (!map[key]) {
      map[key] = { artist: key, gigsCount: 0, totalSongs: 0 }
    }
    map[key].gigsCount += 1
    map[key].totalSongs += gig.total_songs ?? 0
  }
  return Object.values(map).sort((a, b) =>
    b.gigsCount - a.gigsCount || b.totalSongs - a.totalSongs
  )
}

export function buildSongFrequency(gigs) {
  const freq = {}
  for (const gig of gigs) {
    for (const song of gig.top_songs ?? []) {
      freq[song] = (freq[song] ?? 0) + 1
    }
  }
  return Object.entries(freq)
    .map(([song, count]) => ({ song, count }))
    .sort((a, b) => b.count - a.count)
}

export function buildVenueStats(gigs) {
  const map = {}
  for (const gig of gigs) {
    const key = `${gig.venue}||${gig.city}`
    if (!map[key]) {
      map[key] = { venue: gig.venue, city: gig.city, count: 0 }
    }
    map[key].count += 1
  }
  return Object.values(map)
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
}
