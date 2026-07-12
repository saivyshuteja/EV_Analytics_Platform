import { useState } from 'react'
import { usePredictor } from '../hooks/usePredictor'

export default function Predictor() {
  const predict = usePredictor()
  const [form, setForm] = useState({
    model_year: '',
    make: '',
    ev_type: '',
    electric_range: '',
  })

  const submit = () => {
    predict.mutate({
      model_year: Number(form.model_year),
      make: form.make,
      ev_type: form.ev_type,
      electric_range: Number(form.electric_range),
    })
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-2xl shadow-sm">
        <h2 className="text-xl font-semibold">Predict CAFV Eligibility</h2>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <input
          className="p-3 rounded-xl border border-slate-200"
          placeholder="Model Year"
          value={form.model_year}
          onChange={(e) => setForm({ ...form, model_year: e.target.value })}
        />
        <input
          className="p-3 rounded-xl border border-slate-200"
          placeholder="Make"
          value={form.make}
          onChange={(e) => setForm({ ...form, make: e.target.value })}
        />
        <input
          className="p-3 rounded-xl border border-slate-200"
          placeholder="EV Type"
          value={form.ev_type}
          onChange={(e) => setForm({ ...form, ev_type: e.target.value })}
        />
        <input
          className="p-3 rounded-xl border border-slate-200"
          placeholder="Electric Range"
          value={form.electric_range}
          onChange={(e) => setForm({ ...form, electric_range: e.target.value })}
        />
      </div>
      <button
        className="bg-slate-900 text-white px-6 py-3 rounded-xl"
        onClick={submit}
      >
        Predict
      </button>
      {predict.data && (
        <pre className="bg-slate-950 text-white p-6 rounded-2xl">
          {JSON.stringify(predict.data, null, 2)}
        </pre>
      )}
    </div>
  )
}
