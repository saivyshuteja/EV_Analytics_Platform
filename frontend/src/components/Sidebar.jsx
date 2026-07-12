import { Link } from 'react-router-dom'

export default function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white p-6">
      <h1 className="text-2xl font-bold mb-8">EV Analytics</h1>
      <nav className="flex flex-col gap-4 text-sm">
        <Link to="/" className="hover:text-sky-400">Dashboard</Link>
        <Link to="/statistics" className="hover:text-sky-400">Statistics</Link>
        <Link to="/predictor" className="hover:text-sky-400">Predictor</Link>
        <Link to="/models" className="hover:text-sky-400">ML Models</Link>
        <Link to="/rag" className="hover:text-sky-400">RAG Search</Link>
        <Link to="/agent" className="hover:text-sky-400">AI Agent</Link>
      </nav>
    </aside>
  )
}
