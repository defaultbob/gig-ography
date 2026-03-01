import { GigCard } from '@/components/GigCard'

export function GigGrid({ gigs }) {
  if (!gigs.length) {
    return (
      <div className="text-center py-20 text-gray-400">
        <p className="text-lg">No gigs found.</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {gigs.map((gig, i) => (
        <GigCard key={`${gig.headliners.join('-')}-${gig.date}-${i}`} gig={gig} />
      ))}
    </div>
  )
}
