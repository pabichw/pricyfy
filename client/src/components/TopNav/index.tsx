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
    <li className="text-slate-500 font-semibold">
      <Link to={to}>{children}</Link>
    </li>
  )
}

function TopNav(): React.ReactElement {
  return (
    <nav className="sticky flex h-[4rem] top-0 bg-white px-5 z-50 w-100 items-center justify-end md:justify-center shadow-sm">
      <a className="absolute box-content inset-y-3 inset-x-4 lg:inset-x-8 w-11 shadow-md shadow-indigo-300 hover:shadow-lime-300 transition-shadow duration-500" href="/">
        <Logo />
      </a>
      <ul className="flex gap-4 md:gap-10 justify-center items-center">
        <NavItem to="/">Home</NavItem>
        <NavItem to="/browse">Browse</NavItem>
        <NavItem to="/about">About</NavItem>
      </ul>
    </nav>
  )
}

