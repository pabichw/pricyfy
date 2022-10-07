interface TData {
	url: string
	threshold_price: string
	email: string
	token: string
}

const ROOT_URL = import.meta.env.VITE_API_URL as string

export default async function postProductWatch(
	data: TData
): Promise<{ status: string; data: { msg: string } }> {
	const response = await fetch(`${ROOT_URL}/products/watch`, {
		headers: { Accept: 'application/json', 'Content-type': 'application/json' },
		method: 'POST',
		body: JSON.stringify(data)
	})

	return response.json() as Promise<{ status: string; data: { msg: string } }>
}
