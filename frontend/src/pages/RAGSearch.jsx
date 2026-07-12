import { useState } from 'react'
import api from '../services/api'

export default function RAGSearch() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')

  const ask = async () => {
    const res = await api.post('/rag/ask', { question })
    setAnswer(res.data.answer)
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl shadow-sm">
        <h2 className="text-xl font-semibold">RAG Knowledge Search</h2>
      </div>
      <div className="bg-white p-6 rounded-2xl shadow-sm space-y-4">
        <textarea
          className="w-full p-4 border border-slate-200 rounded-2xl"
          rows={4}
          placeholder="Ask a question about EVs, CAFV, or your dataset"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          className="bg-slate-900 text-white px-6 py-3 rounded-xl"
          onClick={ask}
        >
          Ask
        </button>
      </div>
      {answer && (
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <h3 className="text-lg font-semibold">Answer</h3>
          <p className="mt-3 text-slate-700">{answer}</p>
        </div>
      )}
    </div>
  )
}
