export function Header({ page, onPageChange }) {
  const tabs = [
    { id: 'archive', label: 'Seen' },
    { id: 'upcoming', label: 'Upcoming' },
    { id: 'analytics', label: 'Analytics' },
  ]

  return (
    <header className="bg-transparent border-b border-gray-700 sticky top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold text-primary-text tracking-tight">Gig-ography</span>
            <span className="text-gray-500 text-sm font-light hidden sm:inline">/ a lifetime of gigs</span>
          </div>
          <nav className="flex gap-1" role="navigation" aria-label="Main">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => onPageChange(tab.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  page === tab.id
                    ? 'bg-accent text-white'
                    : 'text-gray-400 hover:bg-gray-800'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>
    </header>
  )
}
