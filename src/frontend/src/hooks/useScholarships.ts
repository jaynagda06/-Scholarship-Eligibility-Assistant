import { useState } from 'react'

export default function useScholarships() {
  const [data, setData] = useState(null)
  return { scholarships: data || [], setData }
}
