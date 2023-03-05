import type { HttpStatusCodes, Product } from '../types/types'

const ROOT_URL = import.meta.env.VITE_API_URL as string

interface ProductsResponse {
  // extend GenericGetResponse or something
  status: HttpStatusCodes
  data: { products: [Product] }
}

export async function getProducts({
  fetchFn
}: {
  fetchFn: Function | null
}): Promise<ProductsResponse> {
  if (!fetchFn) {
    throw new Error('No fetch function passed')
  }

  const response = await fetchFn(`${ROOT_URL}/products`, {
    headers: { Accept: 'application/json', 'Content-type': 'application/json' },
    method: 'GET'
  })

  return response.json() as Promise<ProductsResponse>
}

interface RecentProductsResponse {
  // extend GenericGetResponse or something
  status: HttpStatusCodes
  data: { products: [Product] }
}

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
  getProducts,
  getRecentProducts
}
