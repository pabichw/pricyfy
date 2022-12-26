import type { Product } from 'types/types'
import ProductShowcaseItem from './components/ProductsShowcaseItem'

interface Properties {
	products: Product[]
	title?: string
}

function ProductShowcase({ products, title }: Properties): JSX.Element {
	return (
		<section>
			{title && <h1 className='text-xl'>{title}</h1>}
			<ul className='mt-5 grid gap-2'>
				{products?.map((product, idx) => (
					<ProductShowcaseItem key={`${product.product_id}-${idx}`} data={product} />
				))}
			</ul>
		</section>
	)
}

export default ProductShowcase
