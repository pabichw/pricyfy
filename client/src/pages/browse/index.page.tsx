import Head from 'components/Head'
import ProductsShowcase from 'components/ProductsShowcase'
import type { ReactElement } from 'react'
import type { Product } from 'types/types'

export { Page }

interface Properties {
  products: Product[]
}

function Page({ products }: Properties): ReactElement {
  return (
    <>
      <Head title='Pricyfy - Browse offers' />
      <div className='max-w-[60rem] mx-auto mt-12 flex flex-col items-center justify-center p-2 '>
        <header className='mb-8 text-2xl text-center'>Browse monitored ads</header>
        <p className='mb-8 text-s text-center'>All monitored offers are presented down below. Advanced search to be introduced later on.</p>
        <ProductsShowcase products={products} />
      </div>
    </>
  )
}
