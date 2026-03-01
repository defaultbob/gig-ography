/**
 * Pure functions for filtering and sorting the gig array.
 */

export function sortGigsByDate(gigs, direction = 'desc') {
  return [...gigs].sort((a, b) => {
    const diff = new Date(b.date) - new Date(a.date)
    return direction === 'desc' ? diff : -diff
  })
}

export function filterGigs(gigs, query) {
  if (!query) return gigs
  const q = query.toLowerCase()
  return gigs.filter(
    (g) =>
      g.headliners.some((a) => a.toLowerCase().includes(q)) ||
      g.venue.toLowerCase().includes(q) ||
      g.city.toLowerCase().includes(q)
  )
}

export function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = dateStr instanceof Date ? dateStr : new Date(dateStr + 'T00:00:00')
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
}

export function formatYear(dateStr) {
  if (!dateStr) return ''
  return dateStr.slice(0, 4)
}
