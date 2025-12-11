import { Routes, Route } from 'react-router-dom'
import GraphDebug from './pages/GraphDebug'

function App() {
  return (
    <Routes>
      <Route path="/" element={<GraphDebug />} />
    </Routes>
  )
}

export default App
