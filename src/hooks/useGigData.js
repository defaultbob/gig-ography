import { useMemo } from 'react'
import { sortGigsByDate } from '@/utils/dataTransformers'

function normalizeGig(gig) {
  return {
    ...gig,
    top_songs: gig.top_songs ?? [],
    festival_artists: gig.festival_artists ?? [],
    artists_seen: gig.artists_seen ?? [],
    streaming: gig.streaming ?? { spotify: null, apple: null },
  }
}

export function useGigData(gigsRaw) {
  return useMemo(() => {
    const normalized = (gigsRaw ?? []).map(normalizeGig)
    return sortGigsByDate(normalized)
  }, [gigsRaw])
}
