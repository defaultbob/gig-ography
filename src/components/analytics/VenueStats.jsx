export function VenueStats({ data }) {
  const max = data[0]?.count ?? 1

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
      <h2 className="text-lg font-bold text-gray-900 mb-4">Top Venues</h2>
      {data.length === 0 ? (
        <p className="text-gray-400 text-sm">No venue data yet.</p>
      ) : (
        <ul className="space-y-3">
          {data.map(({ venue, city, count }) => (
            <li key={`${venue}-${city}`}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-gray-800 truncate pr-2">{venue}</span>
                <span className="text-gray-400 shrink-0">{count}×</span>
              </div>
              <p className="text-xs text-gray-400 mb-1">{city}</p>
              <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-purple-400 rounded-full"
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
