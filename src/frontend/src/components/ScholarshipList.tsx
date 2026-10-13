import { useState, useEffect } from 'react'

export default function ScholarshipList({ scholarships = [] }) {
  const [items, setItems] = useState(scholarships)
  useEffect(() => {
    setItems(scholarships)
  }, [scholarships])
  if (!items.length) {
    return <p>No scholarships found.</p>
  }
  return (
    <ul>
      {items.map((s) => (
        <li key={s.id}>
          <strong>{s.name}</strong>
          <span>{s.org} | {s.deadline}</span>
          <button>View Details</button>
        </li>
      ))}
    </ul>
  )
}
