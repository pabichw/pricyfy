import ProductsShowcase, { ProductsShowcaseTypes } from 'components/ProductsShowcase'
import Head from 'components/Head'
import type { ReactElement } from 'react'
import Promo from './components/Promo'

export default function HomePage(): ReactElement {
	return (
		<>
			<Head title='Pricyfy' />
			<div className='p-2 max-w-[55rem] flex flex-col mx-auto items-center justify-center '>
				<Promo />
				<div className='my-12 -space-y-px rounded-md'>
					<ProductsShowcase type={ProductsShowcaseTypes.RECENT} />
				</div>
			</div>
		</>
	)
}
