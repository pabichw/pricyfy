import Card from 'components/_atoms/Card'
import type { ReactElement } from 'react'
import ProductAdd from 'components/ProductAdd'

export default function Promo(): ReactElement {
	return (
		<Card noSpacing>
      <div className="flex lg:flex-row flex-col">
        <div className='m-4 min-w-[250px]'>
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
        <div className='p-4 flex flex-col justify-center bg-gradient-to-br from-indigo-600 to-indigo-800 text-white min-h-[150px] w-80'>
          <h3 className='font-bold text-xl'>Keep an eye on your ads.</h3>
          <h5 className='text-m'>It's 100% free</h5>
        </div>
      </div>
		</Card>
	)
}
