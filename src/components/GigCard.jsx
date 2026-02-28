import { useState } from 'react'
import { Badge } from '@/components/ui/Badge'
import { StreamingLinks } from '@/components/ui/StreamingLinks'
import { formatDate } from '@/utils/dataTransformers'

const PLACEHOLDER =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect width='400' height='300' fill='%23e5e7eb'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='14' fill='%239ca3af'%3ENo Image%3C/text%3E%3C/svg%3E"

export function GigCard({ gig }) {
  const [imgSrc, setImgSrc] = useState(gig.image_url || PLACEHOLDER)

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden flex flex-col hover:shadow-md transition-shadow duration-200">
      <div className="aspect-video bg-gray-100 overflow-hidden">
        <img
          src={imgSrc}
          alt={`${gig.artist} live`}
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

        {gig.total_songs != null && (
          <p className="text-xs text-gray-400 mt-2">{gig.total_songs} songs</p>
        )}

        {gig.top_songs.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {gig.top_songs.slice(0, 3).map((song) => (
              <span key={song} className="bg-gray-50 text-gray-600 text-xs px-2 py-0.5 rounded-full border border-gray-200">
                {song}
              </span>
            ))}
          </div>
        )}

        {gig.setlist_url && (
          <a
            href={gig.setlist_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-blue-500 hover:text-blue-700 mt-2 inline-block"
          >
            View setlist →
          </a>
        )}

        <div className="mt-auto pt-3">
          <StreamingLinks streaming={gig.streaming} />
        </div>
      </div>
    </div>
  )
}
