import { formatPrice } from 'components/utils/Price'
import type { Product } from 'types/types'

interface Properties {
	data: Product
}

function ProductsShowcaseItem({ data }: Properties): JSX.Element {
	return (
		<li className='group h-[6rem] rounded-md bg-white p-3 text-gray-800 shadow-md transition hover:shadow-xl'>
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
				<span className='col-span-3 text-sm group-hover:underline'>
					{data.product_id}
				</span>
				<span className='col-span-1 text-right font-bold'>
					{formatPrice(data.last_found_price, { code: 'PLN', symbol: 'zł' })}
				</span>
			</a>
		</li>
	)
}

export default ProductsShowcaseItem
