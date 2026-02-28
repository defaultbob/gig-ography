export function ArtistLeaderboard({ data }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <h2 className="text-lg font-bold text-gray-900 mb-4">Artist Leaderboard</h2>
      {data.length === 0 ? (
        <p className="text-gray-400 text-sm">No data yet.</p>
      ) : (
        <ol className="divide-y divide-gray-50">
          {data.map((row, i) => (
            <li key={row.artist} className="flex items-center gap-4 py-3">
              <span className="w-6 text-sm font-semibold text-gray-400 text-right shrink-0">
                {i + 1}
              </span>
              <span className="flex-1 font-medium text-gray-900 text-sm truncate">{row.artist}</span>
              <span className="text-sm text-gray-500 shrink-0">
                {row.gigsCount} {row.gigsCount === 1 ? 'gig' : 'gigs'}
              </span>
              {row.totalSongs > 0 && (
                <span className="text-xs text-gray-400 shrink-0">{row.totalSongs} songs</span>
              )}
            </li>
          ))}
        </ol>
      )}
    </div>
  )
}
