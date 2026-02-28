import { useState } from 'react'
import { Badge } from '@/components/ui/Badge'
import { FestivalArtistSelector } from '@/components/FestivalArtistSelector'
import { formatDate } from '@/utils/dataTransformers'

const PLACEHOLDER =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect width='400' height='300' fill='%23f3e8ff'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='14' fill='%23a78bfa'%3ENo Poster%3C/text%3E%3C/svg%3E"

export function FestivalCard({ gig }) {
  const [imgSrc, setImgSrc] = useState(gig.image_url || PLACEHOLDER)

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col hover:shadow-md transition-shadow duration-200">
      <div className="aspect-video bg-purple-50 overflow-hidden">
        <img
          src={imgSrc}
          alt={`${gig.artist} poster`}
          className="w-full h-full object-cover"
          onError={() => setImgSrc(PLACEHOLDER)}
        />
      </div>
      <div className="p-4 flex flex-col flex-1">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-bold text-gray-900 text-base leading-tight">{gig.artist}</h3>
          <Badge type={gig.type} />
        </div>
        <p className="text-sm text-gray-500 mt-1">{formatDate(gig.date)}</p>
        <p className="text-sm text-gray-700 mt-0.5">
          {gig.venue}, {gig.city}
        </p>

        <FestivalArtistSelector
          festivalArtists={gig.festival_artists}
          artistsSeen={gig.artists_seen}
        />
      </div>
    </div>
  )
}
