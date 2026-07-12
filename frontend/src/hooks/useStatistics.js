import { useQuery } from '@tanstack/react-query'
import api from '../services/api'

export const useTopMakes = () => {
  return useQuery({
    queryKey: ['top-makes'],
    queryFn: async () => {
      const res = await api.get('/stats/top-makes')
      return res.data
    },
  })
}
