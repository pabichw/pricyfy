import spinner from 'assets/svg/spinner.svg'

interface Properties { children: React.ReactNode, isLoading: boolean, type: 'button' | 'reset' | 'submit' | undefined, onClick?: () => {}}

function Button(Properties_: Properties): JSX.Element {
	const { children, isLoading, type, onClick = (): void => {}} = Properties_
	
	return (
		<button
			className={`
				group relative flex items-center gap-2 w-full justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white 
			hover:bg-indigo-700 
				focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
				disabled:bg-gray-300
			`}
			type={type}
			onClick={onClick}
		>
			{isLoading ? <img className='scale-75' src={spinner} alt='spinner loader' /> : undefined}
			{children}
		</button>
	)
}

export default Button
