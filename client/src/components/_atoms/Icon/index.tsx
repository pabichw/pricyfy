interface Properties extends React.HTMLProps<HTMLInputElement> {
	scale?: number
}

function Icon({ children, scale = 1, ...properties }: Properties): JSX.Element {
	return (
		<div className='w-full bg-amber-100 text-center'>
			<span
				className='inline-block'
				style={{ transform: `scale(${scale})` }}
				{...properties}
			>
				{children}
			</span>
		</div>
	)
}

export default Icon
