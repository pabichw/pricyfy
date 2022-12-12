import ProductShowcaseItem from './components/ProductsShowcaseItem'
import { getRecentProducts } from '../../api/getProducts';
import { useEffect, useState } from 'react'
import type { Product } from 'types/types';

export enum ProductsShowcaseTypes {
	RECENT = 'recent'
}

interface Properties {
	type: ProductsShowcaseTypes
}

const CONTENT_MAP = {
	[ProductsShowcaseTypes.RECENT]: {
		fetchRequest: getRecentProducts,
		title: 'Recently added'
	}
}

function ProductShowcase({ type }: Properties): JSX.Element {
	const [products, setProducts] = useState<Product[] | null>(null);

	useEffect(() => {
		async function doFetch(): Promise<void> {
			const { data }  = await CONTENT_MAP[type].fetchRequest();
			setProducts(data.products)
		}

		doFetch()
	}, [type])

	return (
		<section>
			<h1 className='text-xl'>{CONTENT_MAP[type].title}</h1>
			<ul className='mt-5 grid gap-2'>
				{products?.map(product => <ProductShowcaseItem key={product.product_id} data={product} />)}
			</ul>
		</section>	
	)
}

export default ProductShowcase
