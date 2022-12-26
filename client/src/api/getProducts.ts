import type { HttpStatusCodes, Product } from '../types/types'

interface RecentProductsResponse {
	// extend GenericGetResponse or something
	status: HttpStatusCodes
	data: { products: [Product] }
}

const ROOT_URL = import.meta.env.VITE_API_URL as string

export async function getRecentProducts({
	fetchFn
}: {
	fetchFn: Function | null
}): Promise<RecentProductsResponse> {
	if (!fetchFn) {
		throw new Error('No fetch function passed')
	}

	const response = await fetchFn(`${ROOT_URL}/products/recent`, {
		headers: { Accept: 'application/json', 'Content-type': 'application/json' },
		method: 'GET'
	})

	return response.json() as Promise<RecentProductsResponse>
}

export default {
	getRecentProducts
}
