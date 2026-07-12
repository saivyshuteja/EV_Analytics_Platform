import { useTopMakes } from '../hooks/useStatistics'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function Statistics() {
  const { data, isLoading } = useTopMakes()

  if (isLoading) {
    return <p>Loading...</p>
  }

  const chartData = Object.entries(data || {}).map(([name, value]) => ({
    name,
    value,
  }))

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl shadow-sm">
        <h2 className="text-xl font-semibold">Top EV Makes</h2>
      </div>
      <div className="bg-white p-6 rounded-2xl shadow-sm">
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#0ea5e9" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
