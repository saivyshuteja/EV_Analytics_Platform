import { useState } from 'react'
import { useAgent } from '../hooks/useAgent'

export default function AIAgent() {
  const [query, setQuery] = useState('')
  const agent = useAgent()

  const ask = () => {
    agent.mutate(query)
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl shadow-sm">
        <h2 className="text-xl font-semibold">AI Agent Chat</h2>
      </div>
      <div className="bg-white p-6 rounded-2xl shadow-sm space-y-4">
        <input
          className="w-full p-3 border border-slate-200 rounded-2xl"
          placeholder="Ask the EV agent a question"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          className="bg-slate-900 text-white px-6 py-3 rounded-xl"
          onClick={ask}
        >
          Chat
        </button>
      </div>
      {agent.data && (
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <h3 className="text-lg font-semibold">Agent Response</h3>
          <pre className="mt-3 whitespace-pre-wrap text-slate-700">{JSON.stringify(agent.data, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
