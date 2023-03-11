export enum ProductStatus {
  RUNNING = 'RUNNING',
  JUST_ADDED = 'JUST_RUNNING',
  INACTIVE = 'INACTIVE'
}

export interface Product {
  _id: string
  product_id: string
  images?: []
  last_found_price?: number
  status: ProductStatus
  url: string
  price_history: HistoryEntry[] | undefined
}

export enum HttpStatusCodes {
  OK = 200
}

export interface Currency {
  code: string
  symbol: string
}

export interface HistoryEntry {
  _id: string
  price_parsed: string
  parse_time: string
}

export interface StatisticsDTO {
  created_at: string
  count: number
  average_change: number
  works_since: string
}

export type LastStatisticsDTO = StatisticsDTO
