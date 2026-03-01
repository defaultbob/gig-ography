export function FestivalArtistSelector({ lineup, artistsSeen }) {
  if (!lineup.length) return null
  const seenSet = new Set(artistsSeen.map((a) => a.toLowerCase()))
  return (
    <div className="mt-3">
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1.5">Lineup</p>
      <div className="flex flex-wrap gap-1.5">
        {lineup.map((artist) => {
          const seen = seenSet.has(artist.toLowerCase())
          return (
            <span
              key={artist}
              className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                seen
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-500'
              }`}
            >
              {artist}
            </span>
          )
        })}
      </div>
      {artistsSeen.length > 0 && (
        <p className="text-xs text-gray-400 mt-1.5">
          Highlighted = artists you saw
        </p>
      )}
    </div>
  )
}
