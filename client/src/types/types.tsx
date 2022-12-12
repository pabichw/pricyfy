export enum ProductStatus {
	ACTIVE = '',
	INACTIVE = 'INACTIVE'
}

export interface Product {
	_id: string
	product_id: string
	images: [string]
	last_found_price: number
	status: ProductStatus
	url: string
}

export enum HttpStatusCodes {
	OK = 200
}

export interface Currency {
  code: string 
  symbol: string
}