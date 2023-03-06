import Head from 'components/Head'
import ProductsShowcase from 'components/ProductsShowcase'
import type { ReactElement } from 'react'
import type { Product } from 'types/types'
import Promo from './Home/components/Promo'

export { Page }

interface Properties {
  recentProducts: Product[]
}

function Page({ recentProducts }: Properties): ReactElement {
  return (
    <>
      <Head title='Pricyfy' />
      <div className='mx-auto mt-16 flex max-w-[55rem] flex-col items-center justify-center p-2 md:p-0'>
        <Promo />
        <div className='my-16 -space-y-px rounded-md'>
          <ProductsShowcase
            products={recentProducts}
            title='Recently uploaded'
          />
        </div>
      </div>
    </>
  )
}
