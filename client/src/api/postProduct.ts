interface TData {
	url: string
	email: string
	token: string
}

const ROOT_URL = import.meta.env.VITE_API_URL as string

export async function postProductWatch(
	data: TData
): Promise<{ status: string; data: { msg: string }, error: { msg: string } }> {
	const response = await fetch(`${ROOT_URL}/products/watch`, {
		headers: { Accept: 'application/json', 'Content-type': 'application/json' },
		method: 'POST',
		body: JSON.stringify(data)
	})

	return response.json() as Promise<{ status: string; data: { msg: string }; error: { msg: string } }>
}

export default {
	postProductWatch
}