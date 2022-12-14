import Card from 'components/_atoms/Card'
import type { ReactElement } from 'react'
import ProductAdd from 'components/ProductAdd'

export default function Promo(): ReactElement {
	return (
		<Card>
			<div className='mb-5'>
				<p className='pb-1 text-center text-3xl font-bold tracking-wide text-gray-800'>
					Pricyfy
				</p>
				<p className='text-m font-regular text-center tracking-wide text-gray-500'>
					Monitor ads prices
				</p>
			</div>
			<ProductAdd />
		</Card>
	)
}
