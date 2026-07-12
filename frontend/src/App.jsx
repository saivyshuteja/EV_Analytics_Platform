import Sidebar from './components/Sidebar'
import Header from './components/Header'
import AppRoutes from './routes/AppRoutes'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="flex">
        <Sidebar />
        <div className="flex-1">
          <Header />
          <main className="p-6">
            <AppRoutes />
          </main>
        </div>
      </div>
    </div>
  )
}
