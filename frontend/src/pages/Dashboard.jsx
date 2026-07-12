export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <h3 className="text-sm text-slate-500">Total Vehicles</h3>
          <p className="mt-3 text-3xl font-semibold">210,166</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <h3 className="text-sm text-slate-500">RAG Chunks</h3>
          <p className="mt-3 text-3xl font-semibold">500+</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <h3 className="text-sm text-slate-500">Models</h3>
          <p className="mt-3 text-3xl font-semibold">6</p>
        </div>
      </div>
      <div className="bg-white p-6 rounded-2xl shadow-sm">
        <h3 className="text-lg font-semibold">EV Analytics AI Platform</h3>
        <p className="mt-3 text-slate-600">
          Explore vehicle prediction, model comparisons, RAG search, and statistical insights.
        </p>
      </div>
    </div>
  )
}
