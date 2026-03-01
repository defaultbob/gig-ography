import { useMemo } from 'react'
import { sortGigsByDate } from '@/utils/dataTransformers'

function normalizeGig(gig) {
  return {
    ...gig,
    headliners: gig.headliners ?? [],
    support: gig.support ?? [],
    lineup: gig.lineup ?? [],
    artists_seen: gig.artists_seen ?? [],
  }
}

export function useGigData(gigsRaw) {
  return useMemo(() => {
    const normalized = (gigsRaw ?? []).map(normalizeGig)
    return sortGigsByDate(normalized)
  }, [gigsRaw])
}
