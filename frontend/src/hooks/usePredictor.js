import { useMutation } from '@tanstack/react-query'
import api from '../services/api'

export const usePredictor = () => {
  return useMutation({
    mutationFn: async (data) => {
      const res = await api.post('/ml/predict', data)
      return res.data
    },
  })
}
