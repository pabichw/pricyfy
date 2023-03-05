import React, { ReactNode } from 'react'

export { Link }

interface LinkProperties {
  to: string,
  children: ReactNode
}

function Link({ to, children }: LinkProperties): React.ReactElement {
  return (
    <a className="hover:text-indigo-800 transition-colors" href={to}>{children}</a>
  )
}

