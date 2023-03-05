import React, { ReactNode } from 'react'
import { Logo } from 'components/Logo'
import { Link } from 'components/Link'

export { TopNav }

interface NavItemProperties {
  to: string,
  children: ReactNode
}

function NavItem({ to, children }: NavItemProperties): React.ReactElement {
  return (
    <li className="text-neutral-400 font-bold">
      <Link to={to}>{children}</Link>
    </li>
  )
}

function TopNav(): React.ReactElement {
  return (
    <nav className="sticky flex h-[4rem] top-0 bg-white z-50 w-screen items-center justify-center shadow-black">
      <a className="absolute inset-y-3 inset-x-8 w-11" href="/">
        <Logo />
      </a>
      <ul className="flex gap-10 justify-center items-center">
        <NavItem to="/">Home</NavItem>
        <NavItem to="/about">About</NavItem>
      </ul>
    </nav>
  )
}

