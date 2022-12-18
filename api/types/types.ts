export enum ProductStatus {
	RUNNING = 'RUNNING',
	JUST_ADDED = 'JUST_ADDED',
	INACTIVE = 'INACTIVE'
}

export interface Product {
	product_id: string
	images?: []
	last_found_price?: number
	status: ProductStatus
	url: string
}

export interface ProductQueueEntry {
  url: string
  threshold_price: number
  recipients: [string]
}

export interface HistoryEntry {
  product_id: string
  product_title: string
  price_parsed: number
  price_threshold: number
  parese_time: string
}
