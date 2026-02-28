export function FilterBar({ query, onQueryChange, sortDir, onSortDirChange, total, filtered }) {
  return (
    <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between mb-8">
      <div className="relative flex-1 max-w-sm">
        <svg
          className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="search"
          placeholder="Search artist, venue or city…"
          value={query}
          onChange={(e) => onQueryChange(e.target.value)}
          className="w-full pl-9 pr-4 py-2 rounded-xl border border-gray-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-300 placeholder-gray-400"
        />
      </div>
      <div className="flex items-center gap-3 text-sm text-gray-500">
        <span>
          {filtered === total ? total : `${filtered} of ${total}`} gigs
        </span>
        <button
          onClick={() => onSortDirChange(sortDir === 'desc' ? 'asc' : 'desc')}
          className="flex items-center gap-1 px-3 py-1.5 rounded-lg border border-gray-200 bg-white hover:bg-gray-50 transition-colors text-gray-600"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={sortDir === 'desc' ? 'M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4' : 'M3 4h13M3 8h9m-9 4h6m4 0v12m0 0l-4-4m4 4l4-4'} />
          </svg>
          {sortDir === 'desc' ? 'Newest first' : 'Oldest first'}
        </button>
      </div>
    </div>
  )
}
