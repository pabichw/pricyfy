// import getFruits from 'api/getFruits'
// import Fruit from 'components/Fruit'
import Head from 'components/Head'
// import LoadingOrError from 'components/LoadingOrError'
import type { ReactElement } from 'react'
// import { useQuery } from '@tanstack/react-query'
import ProductAdd from 'components/ProductAdd'

export default function HomePage(): ReactElement {
	// const { isLoading, isError, error, data } = useQuery(['fruits'], getFruits)
	// if (isLoading || isError) {
	// 	return <LoadingOrError error={error as Error} />
	// }

	return (
		<>
			<Head title='Pricyfy' />
			<div className='m-2 flex min-h-screen items-center justify-center '>
				<div className='-space-y-px rounded-md bg-white px-3 py-4 shadow-sm '>
					<div className='mb-5'>
						<p className='pb-1 text-center text-3xl font-bold tracking-wide text-gray-800'>
							Pricyfy
						</p>
						<p className='text-m font-regular text-center tracking-wide text-gray-500'>
							Monitor ads price
						</p>
					</div>
					<ProductAdd />
				</div>
			</div>
		</>
	)
}
