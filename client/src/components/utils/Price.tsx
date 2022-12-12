import type { Currency } from 'types/types'

interface Options { 
  separator: ' ' | ',' | '.'
}

const defaultOptions: Options = { separator: ' ' }

export const formatPrice = (input: number | string, currency: Currency, options: Options = defaultOptions): string =>
	// eslint-disable-next-line unicorn/no-unsafe-regex
	`${Number.parseFloat(input.toString()).toString().replace(/\B(?=(\d{3})+(?!\d))/g, options.separator)} ${currency.symbol}`

export default { formatPrice }