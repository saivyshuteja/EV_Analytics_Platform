import { useMutation } from '@tanstack/react-query'
import api from '../services/api'

export const useAgent = () => {
  return useMutation({
    mutationFn: async (query) => {
      const res = await api.post('/agent/chat', { query })
      return res.data
    },
  })
}
