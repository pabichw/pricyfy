import { getRecentProducts } from 'api/getProducts'
import nodeFetch from 'node-fetch'

export async function onBeforeRender() {
	const {
		data: { products }
	} = await getRecentProducts({ fetchFn: nodeFetch })

	const pageProps = { recentProducts: products }

	return {
		pageContext: {
			pageProps
		}
	}
}

export const passToClient = ['pageProps']
