import { useState } from 'react'
import gigsRaw from '../data/master_gigs.yaml'
import { useGigData } from '@/hooks/useGigData'
import { Header } from '@/components/layout/Header'
import { Footer } from '@/components/layout/Footer'
import { ArchivePage } from '@/pages/ArchivePage'
import { AnalyticsPage } from '@/pages/AnalyticsPage'

export default function App() {
  const [page, setPage] = useState('archive')
  const gigs = useGigData(gigsRaw)

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header page={page} onPageChange={setPage} />
      {page === 'archive' ? (
        <ArchivePage gigs={gigs} />
      ) : (
        <AnalyticsPage gigs={gigs} />
      )}
      <Footer />
    </div>
  )
}
