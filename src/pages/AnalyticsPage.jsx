import { useAnalytics } from '@/hooks/useAnalytics'
import { ArtistLeaderboard } from '@/components/analytics/ArtistLeaderboard'
import { GlobalSongStats } from '@/components/analytics/GlobalSongStats'
import { VenueStats } from '@/components/analytics/VenueStats'

export function AnalyticsPage({ gigs }) {
  const { artistLeaderboard, songFrequency, venueStats } = useAnalytics(gigs)

  const totalSongs = gigs.reduce((sum, g) => sum + (g.total_songs ?? 0), 0)
  const totalGigs = gigs.length
  const years = gigs.map((g) => g.date?.slice(0, 4)).filter(Boolean)
  const yearSpan = years.length
    ? `${Math.min(...years)} – ${Math.max(...years)}`
    : '—'

  return (
    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
        <StatCard label="Total Gigs" value={totalGigs} />
        <StatCard label="Total Songs Heard" value={totalSongs.toLocaleString()} />
        <StatCard label="Years Active" value={yearSpan} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <ArtistLeaderboard data={artistLeaderboard} />
        <GlobalSongStats data={songFrequency} />
        <VenueStats data={venueStats} />
      </div>
    </main>
  )
}

function StatCard({ label, value }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 text-center">
      <p className="text-3xl font-bold text-gray-900">{value}</p>
      <p className="text-sm text-gray-500 mt-1">{label}</p>
    </div>
  )
}
