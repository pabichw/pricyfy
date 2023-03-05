import React from 'react'

import logo from 'assets/png/logo.png'

export { Logo }

function Logo() {
  return (
    <img className="object-cover h-10 w-fit" src={logo} />
  )
}

