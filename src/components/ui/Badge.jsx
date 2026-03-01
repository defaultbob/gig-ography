export function Badge({ isFestival }) {
  if (!isFestival) return null
  return (
    <span className="inline-block rounded-full px-2 py-0.5 text-xs font-semibold uppercase tracking-wide bg-purple-100 text-purple-800">
      festival
    </span>
  )
}
