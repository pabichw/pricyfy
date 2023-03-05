import { getProducts } from 'api/getProducts'
import nodeFetch from 'node-fetch'

export async function onBeforeRender() {
  const {
    data: { products }
  } = await getProducts({ fetchFn: nodeFetch })

  console.log('server products', products);

  const pageProps = { products }

  return {
    pageContext: {
      pageProps
    }
  }
}

export const passToClient = ['pageProps']
