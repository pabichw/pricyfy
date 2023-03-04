import Head from 'components/Head'
import ProductsShowcase from 'components/ProductsShowcase'
import type { ReactElement } from 'react'
import type { Product } from 'types/types'
import Promo from './Home/components/Promo'

export { Page }

function Page(): ReactElement {
  return (
    <>
      <Head title='Pricyfy - About us' />
      <div className='mx-auto mt-12 flex flex-col items-center justify-center p-2 '>
        <article className='min-w-[55rem] rounded-md bg-white p-8 text-gray-800 shadow-md transition'>
          <header className='mb-3 text-xl text-center'>About us</header>
          <p className='text-s text-justify'>
            Pricify is a free software to <b>monitor price changes</b> of ads from selected, supported advertisements websites.
          </p>
          <p className='text-s text-justify mt-2'>
            Currently we are supporting following websites:
            <ul className='list-disc ml-5 mb-2'>
              <li>OLX</li>
              <li>OtoDom</li>
            </ul>
            More soon to be announced.
          </p>
        </article>
      </div>
    </>
  )
}
