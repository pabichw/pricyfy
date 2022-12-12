import ProductsShowcase, { ProductsShowcaseTypes } from 'components/ProductsShowcase'
import Head from 'components/Head'
import type { ReactElement } from 'react'
import ProductAdd from 'components/ProductAdd'

export default function HomePage(): ReactElement {
	return (
		<>
			<Head title='Pricyfy' />
			<div className='m-2 max-w-[55rem] flex flex-col mx-auto items-center justify-center '>
				<div className='my-12 -space-y-px rounded-md bg-white px-3 py-4 shadow-md'>
					<div className='mb-5'>
						<p className='pb-1 text-center text-3xl font-bold tracking-wide text-gray-800'>
							Pricyfy
						</p>
						<p className='text-m font-regular text-center tracking-wide text-gray-500'>
							Monitor ads prices
						</p>
					</div>
					<ProductAdd />
				</div>
				<div className='my-12 -space-y-px rounded-md'>
					<ProductsShowcase type={ProductsShowcaseTypes.RECENT} />
				</div>
			</div>
		</>
	)
}
