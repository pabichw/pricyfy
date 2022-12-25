import Head from 'components/Head'
import ProductsShowcase, {
	ProductsShowcaseTypes
} from 'components/ProductsShowcase'
import type { ReactElement } from 'react'
import Promo from './Home/components/Promo'

export { Page }

function Page(): ReactElement {
	return (
		<>
			<Head title='Pricyfy' />
			<div className='mx-auto mt-12 flex max-w-[55rem] flex-col items-center justify-center p-2 '>
				<Promo />
				<div className='my-12 -space-y-px rounded-md'>
					<ProductsShowcase type={ProductsShowcaseTypes.RECENT} />
				</div>
			</div>
		</>
	)
}
