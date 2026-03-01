import { useState } from 'react'
import { Badge } from '@/components/ui/Badge'
import { FestivalArtistSelector } from '@/components/FestivalArtistSelector'
import { formatDate } from '@/utils/dataTransformers'

const PLACEHOLDER =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect width='400' height='300' fill='%23e5e7eb'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='14' fill='%239ca3af'%3ENo Image%3C/text%3E%3C/svg%3E"

export function GigCard({ gig }) {
  const [imgSrc, setImgSrc] = useState(gig.image_url || PLACEHOLDER)
  const isFestival = Boolean(gig.end_date && gig.end_date !== gig.date)
  const dateDisplay = isFestival
    ? `${formatDate(gig.date)} – ${formatDate(gig.end_date)}`
    : formatDate(gig.date)

  return (
    <div className="bg-card-background rounded-2xl shadow-sm border border-gray-700 overflow-hidden flex flex-col hover:shadow-lg transition-shadow duration-200">
      <div className="aspect-video overflow-hidden">
        <img
          src={imgSrc}
          alt={`${gig.headliners.join(', ')} live`}
          className="w-full h-full object-cover"
          onError={() => setImgSrc(PLACEHOLDER)}
        />
      </div>
      <div className="p-4 flex flex-col flex-1">
        <div className="flex items-start justify-between gap-2">
          <div>
            <h3 className="font-bold text-primary-text text-base leading-tight">
              {gig.event_name || gig.headliners.join(' + ')}
            </h3>
            {gig.event_name && (
              <p className="text-sm text-gray-400">{gig.headliners.join(' + ')}</p>
            )}
          </div>
          <Badge isFestival={isFestival} />
        </div>

        {gig.support.length > 0 && (
          <p className="text-xs text-gray-400 mt-0.5">+ {gig.support.join(', ')}</p>
        )}

        <p className="text-sm text-gray-400 mt-1">{dateDisplay}</p>
        <p className="text-sm text-gray-300 mt-0.5">
          {gig.venue}, {gig.city}
        </p>

        <FestivalArtistSelector lineup={gig.lineup} artistsSeen={gig.artists_seen} />

      </div>
    </div>
  )
}
