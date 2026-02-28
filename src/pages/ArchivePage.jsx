import { useState } from 'react'
import { GigGrid } from '@/components/GigGrid'
import { FilterBar } from '@/components/FilterBar'
import { filterGigs, sortGigsByDate } from '@/utils/dataTransformers'

export function ArchivePage({ gigs }) {
  const [query, setQuery] = useState('')
  const [sortDir, setSortDir] = useState('desc')

  const filtered = filterGigs(gigs, query)
  const sorted = sortGigsByDate(filtered, sortDir)

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <FilterBar
        query={query}
        onQueryChange={setQuery}
        sortDir={sortDir}
        onSortDirChange={setSortDir}
        total={gigs.length}
        filtered={filtered.length}
      />
      <GigGrid gigs={sorted} />
    </main>
  )
}
