import React from 'react'
import { PageContextProvider } from './usePageContext'
import type { PageContext } from './types'

import { Toaster } from 'react-hot-toast';

function Layout({ children }: { children: React.ReactNode }): JSX.Element {
  return (
    <div>
      {children}
    </div>
  )
}

function PageShell({ children, pageContext }: { children: React.ReactNode; pageContext: PageContext }): JSX.Element {
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

export default PageShell
