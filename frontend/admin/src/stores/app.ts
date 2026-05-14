import { defineStore } from 'pinia'
import { ref } from 'vue'
import { http } from '@/utils/http'

interface SeasonInfo {
  id: number
  name: string
  status: string
}

export const useAppStore = defineStore('app', () => {
  const currentSeason = ref<SeasonInfo | null>(null)

  async function fetchCurrentSeason() {
    try {
      const res = await http.get<any, any>('/public/seasons/current')
      currentSeason.value = res.data
    } catch {
      currentSeason.value = null
    }
  }

  return { currentSeason, fetchCurrentSeason }
})
