import type { HttpStatusCodes, LastStatisticsDTO } from '../types/types'

const ROOT_URL = import.meta.env.VITE_API_URL as string

interface LastStatisticsReponse {
  // extend GenericGetResponse or something
  status: HttpStatusCodes
  data: { statistics: LastStatisticsDTO }
}

export async function getLastStatistics({
  fetchFn
}: {
  fetchFn: Function | null
}): Promise<LastStatisticsReponse> {
  if (!fetchFn) {
    throw new Error('No fetch function passed')
  }

  const response = await fetchFn(`${ROOT_URL}/statistics/last`, {
    headers: { Accept: 'application/json', 'Content-type': 'application/json' },
    method: 'GET'
  })

  return response.json() as Promise<LastStatisticsReponse>
}
