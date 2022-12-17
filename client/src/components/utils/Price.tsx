import type { Currency } from 'types/types'

interface Options { 
  separator: ' ' | ',' | '.'
}

const defaultOptions: Options = { separator: ' ' }

export const formatPrice = (input: number | string | undefined, currency: Currency, options: Options = defaultOptions): string => {
	if (!input) {
		return ''
	}
	// eslint-disable-next-line unicorn/no-unsafe-regex
	return `${Number.parseFloat(input.toString()).toString().replace(/\B(?=(\d{3})+(?!\d))/g, options.separator)} ${currency.symbol}`
}

export default { formatPrice }