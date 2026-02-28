import { useMemo } from 'react'
import {
  buildArtistLeaderboard,
  buildSongFrequency,
  buildVenueStats,
} from '@/utils/analyticsCalculators'

export function useAnalytics(gigs) {
  return useMemo(
    () => ({
      artistLeaderboard: buildArtistLeaderboard(gigs),
      songFrequency: buildSongFrequency(gigs),
      venueStats: buildVenueStats(gigs),
    }),
    [gigs]
  )
}
