import { useState } from 'react'
import gigsRaw from '../data/gigs.yaml'
import { useGigData } from '@/hooks/useGigData'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { ArchivePage } from '@/pages/ArchivePage'
import { AnalyticsPage } from '@/pages/AnalyticsPage'
import { UpcomingPage } from '@/pages/UpcomingPage'

export default function App() {
  const [page, setPage] = useState('upcoming')
  const gigs = useGigData(gigsRaw)

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header page={page} onPageChange={setPage} />
      {page === 'archive' && <ArchivePage gigs={gigs} />}
      {page === 'upcoming' && <UpcomingPage gigs={gigs} />}
      {page === 'analytics' && <AnalyticsPage gigs={gigs} />}
      <Footer />
    </div>
  )
}
