import { getRecentProducts } from 'api/getProducts'
import { getLastStatistics } from 'api/getStatistics'
import nodeFetch from 'node-fetch'

export async function onBeforeRender() {
  const {
    data: { products }
  } = await getRecentProducts({ fetchFn: nodeFetch })

  const {
    data: { statistics }
  } = await getLastStatistics({ fetchFn: nodeFetch })

  const pageProps = { recentProducts: products, lastStatistics: statistics }

  return {
    pageContext: {
      pageProps
    }
  }
}

export const passToClient = ['pageProps']
