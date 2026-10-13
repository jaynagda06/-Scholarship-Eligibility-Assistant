import { useState, useEffect } from 'react'

export default function App() {
  const [scholarships, setScholarships] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('http://localhost:3000/scholarships')
      .then((res) => {
        if (!res.ok) throw new Error('Failed to fetch scholarships')
        return res.json()
      })
      .then((data) => {
        setScholarships(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Scholarship Eligibility Assistant</h1>
      {loading && <p>Loading scholarships...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {!loading && !error && (
        <div style={{ border: '1px solid #ccc', padding: '1rem' }}>
          <h2>Available Scholarships ({scholarships.length})</h2>
          <ul>
            {scholarships.map((s) => (
              <li key={s.id} style={{ marginBottom: '1rem' }}>
                <strong>{s.name}</strong>
                <br />
                <span>{s.org}</span>
                <br />
                <span>Deadline: {s.deadline}</span>
                <br />
                <span>Category: {s.category}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
