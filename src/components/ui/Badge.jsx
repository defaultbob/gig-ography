export function Badge({ type }) {
  const styles =
    type === 'festival'
      ? 'bg-purple-100 text-purple-800'
      : 'bg-blue-100 text-blue-800'
  return (
    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-semibold uppercase tracking-wide ${styles}`}>
      {type}
    </span>
  )
}
