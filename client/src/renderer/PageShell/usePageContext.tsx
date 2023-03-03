import React, { useContext } from 'react'
import type { PageContext } from './types'

const Context = React.createContext<PageContext>(undefined as any)

function PageContextProvider({
  pageContext,
  children
}: {
  pageContext: PageContext
  children: React.ReactNode
}): JSX.Element {
  return <Context.Provider value={pageContext}>{children}</Context.Provider>
}

function usePageContext(): PageContext {
  const pageContext = useContext(Context)
  return pageContext
}

export { PageContextProvider }
export { usePageContext }

