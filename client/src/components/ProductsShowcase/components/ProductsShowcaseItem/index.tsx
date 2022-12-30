import { formatPrice } from 'utils/Price'
import { lazy, Suspense } from 'react'
import type { Product } from 'types/types'
import { canUseDOM } from 'utils/Rendering'
interface Properties {
  data: Product
}

const exampledata = [
	{
		label: 'Series 1',
		data: [
			{
				primary: '2022-12-29',
				secondary: 31
			},
			{
				primary: '2022-12-30',
				secondary: 15
			},
			{
				primary: '2022-12-31',
				secondary: 73
			},
			{
				primary: '2023-01-01',
				secondary: 75
			},
			{
				primary: '2023-01-02',
				secondary: 5
			},
			{
				primary: '2023-01-03',
				secondary: 29
			},
			{
				primary: '2023-01-04',
				secondary: 79
			},
			{
				primary: '2023-01-05',
				secondary: 95
			},
			{
				primary: '2023-01-06',
				secondary: 37
			},
			{
				primary: '2023-01-07',
				secondary: 5
			}
		]
	},
	{
		label: 'Series 2',
		data: [
			{
				primary: '2022-12-29',
				secondary: 54
			},
			{
				primary: '2022-12-30',
				secondary: 40
			},
			{
				primary: '2022-12-31',
				secondary: 29
			},
			{
				primary: '2023-01-01',
				secondary: 100
			},
			{
				primary: '2023-01-02',
				secondary: 90
			},
			{
				primary: '2023-01-03',
				secondary: 51
			},
			{
				primary: '2023-01-04',
				secondary: 0
			},
			{
				primary: '2023-01-05',
				secondary: 87
			},
			{
				primary: '2023-01-06',
				secondary: 43
			},
			{
				primary: '2023-01-07',
				secondary: 40
			}
		]
	}
]

export const Chart: any = canUseDOM() ? lazy(() => import('../../../ChartArea/index')) : null

function ProductsShowcaseItem({ data }: Properties): JSX.Element {
	console.log('can use dom ', canUseDOM())
	return (
		<li className='group h-[12rem] rounded-md bg-white p-3 text-gray-800 shadow-md transition hover:shadow-xl'>
			<a
				href={data.url}
				className='grid h-full w-full grid-cols-5 gap-x-4'
				target='__blank'
				referrerPolicy='no-referrer'
			>
				<span className='col-span-1 mx-auto overflow-hidden'>
					<img
						loading='lazy'
						alt={`product thumbnail ${data._id}`}
						className='max-h-full'
						src={data.images?.[0]}
					/>
				</span>
				<span className='col-span-2 text-sm group-hover:underline'>
					{data.product_id}
				</span>
				<span className='col-span-1'>
					{canUseDOM()
						&& <Suspense fallback="Loading">
								<Chart data={exampledata} /> 
							</Suspense>}
				</span>
				<span className='col-span-1 text-right font-bold'>
					{formatPrice(data.last_found_price, { code: 'PLN', symbol: 'zł' })}
				</span>
			</a>
		</li>
	)
}

export default ProductsShowcaseItem
