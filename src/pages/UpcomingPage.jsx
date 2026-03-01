import { useState } from 'react'
import { GigGrid } from '@/components/GigGrid'
import { FilterBar } from '@/components/FilterBar'
import { filterGigs, sortGigsByDate } from '@/utils/dataTransformers'

export function UpcomingPage({ gigs }) {
  const [query, setQuery] = useState('')
  const [sortDir, setSortDir] = useState('asc')

  const upcomingGigs = gigs.filter(gig => new Date(gig.date) > new Date())
  const filtered = filterGigs(upcomingGigs, query)
  const sorted = sortGigsByDate(filtered, sortDir)

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <FilterBar
        query={query}
        onQueryChange={setQuery}
        sortDir={sortDir}
        onSortDirChange={setSortDir}
        total={upcomingGigs.length}
        filtered={filtered.length}
      />
      <GigGrid gigs={sorted} />
    </main>
  )
}
