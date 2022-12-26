import React from 'react'
import { PageContextProvider } from './usePageContext'
import type {PageContext} from './types'

import { Toaster } from 'react-hot-toast';

function PageShell({ children, pageContext }: { children: React.ReactNode; pageContext: PageContext }) {
  return (
    <React.StrictMode>
      <PageContextProvider pageContext={pageContext}>
        <Layout>
          {children}
        </Layout>
				<Toaster position='top-right' />
      </PageContextProvider>
    </React.StrictMode>
  )
}

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      {children}
    </div>
  )
}

export default PageShell