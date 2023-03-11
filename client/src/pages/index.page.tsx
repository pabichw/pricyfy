import Head from 'components/Head'
import ProductsShowcase from 'components/ProductsShowcase'
import StatsShowcase from 'components/StatsShowcase'
import type { ReactElement } from 'react'
import type { Product, StatisticsDTO } from 'types/types'
import Promo from './Home/components/Promo'

export { Page }

interface Properties {
  lastStatistics: StatisticsDTO[]
  recentProducts: Product[]
}

function Page({ lastStatistics, recentProducts }: Properties): ReactElement {
  return (
    <>
      <Head title='Pricyfy' />
      <div className='mx-auto mt-10 md:mt-24 flex gap-10 md:gap-20 max-w-[55rem] flex-col items-center justify-center p-2 md:p-0'>
        <Promo />
        <div className='w-full'>
          <StatsShowcase stats={lastStatistics} />
        </div>
        <div>
          <ProductsShowcase
            products={recentProducts}
            title='Recently uploaded'
          />
        </div>
      </div>
    </>
  )
}
