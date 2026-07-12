import { Routes, Route } from 'react-router-dom'
import Dashboard from '../pages/Dashboard'
import Statistics from '../pages/Statistics'
import Predictor from '../pages/Predictor'
import MLModels from '../pages/MLModels'
import RAGSearch from '../pages/RAGSearch'
import AIAgent from '../pages/AIAgent'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/statistics" element={<Statistics />} />
      <Route path="/predictor" element={<Predictor />} />
      <Route path="/models" element={<MLModels />} />
      <Route path="/rag" element={<RAGSearch />} />
      <Route path="/agent" element={<AIAgent />} />
    </Routes>
  )
}
