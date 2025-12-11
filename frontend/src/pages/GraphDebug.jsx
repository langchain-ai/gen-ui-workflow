import { useState } from 'react'

export default function GraphDebug() {
  const [prompt, setPrompt] = useState('')
  const [graphState, setGraphState] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [currentNode, setCurrentNode] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setIsLoading(true)
    setError(null)
    setGraphState(null)
    setCurrentNode(null)

    try {
      const response = await fetch('http://localhost:8000/api/generate-ui/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6))

            if (data.state) {
              setCurrentNode(data.node)
              setGraphState(data.state)
            }
          } else if (line.startsWith('event: done')) {
            setIsLoading(false)
            setCurrentNode('complete')
          } else if (line.startsWith('event: error')) {
            setError(JSON.parse(line.slice(6)).error)
            setIsLoading(false)
          }
        }
      }
    } catch (err) {
      setError(err.message)
      setIsLoading(false)
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your UI prompt..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Processing...' : 'Generate'}
        </button>
      </form>

      {currentNode && <p>Current Node: {currentNode}</p>}

      {error && <p>Error: {error}</p>}

      {graphState && <pre>{JSON.stringify(graphState, null, 2)}</pre>}
    </div>
  )
}
