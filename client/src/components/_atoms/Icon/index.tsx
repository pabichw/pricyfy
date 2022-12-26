interface Properties extends React.HTMLProps<HTMLInputElement> {
	translateX?: string
	scale?: number
}

function Icon({ children, translateX, scale = 1, ...properties }: Properties): JSX.Element {
	return (
		<span
			className='inline-block'
			style={{ transform: `scale(${scale}) translateX(${translateX})` }}
			{...properties}
		>
			{children}
		</span>
	)
}

export default Icon
