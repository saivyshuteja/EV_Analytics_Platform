import { useQuery } from '@tanstack/react-query'
import api from '../services/api'

export default function MLModels() {
  const { data, isLoading } = useQuery({
    queryKey: ['models'],
    queryFn: async () => {
      const res = await api.get('/ml/models')
      return res.data
    },
  })

  if (isLoading) {
    return <p>Loading...</p>
  }

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm">
      <h2 className="text-xl font-semibold mb-4">ML Model Comparison</h2>
      <pre className="whitespace-pre-wrap break-words">{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
