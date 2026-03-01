import { useMemo } from 'react'
import {
  buildArtistLeaderboard,
} from '@/utils/analyticsCalculators'

export function useAnalytics(gigs) {
  return useMemo(
    () => ({
      artistLeaderboard: buildArtistLeaderboard(gigs),
    }),
    [gigs]
  )
}
