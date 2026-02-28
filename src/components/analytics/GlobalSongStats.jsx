export function GlobalSongStats({ data }) {
  const top = data.slice(0, 10)
  const max = top[0]?.count ?? 1

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <h2 className="text-lg font-bold text-gray-900 mb-4">Most Heard Songs</h2>
      {top.length === 0 ? (
        <p className="text-gray-400 text-sm">No song data yet.</p>
      ) : (
        <ul className="space-y-3">
          {top.map(({ song, count }) => (
            <li key={song}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-gray-800 truncate pr-2">{song}</span>
                <span className="text-gray-400 shrink-0">{count}×</span>
              </div>
              <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-blue-400 rounded-full"
                  style={{ width: `${(count / max) * 100}%` }}
                />
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
