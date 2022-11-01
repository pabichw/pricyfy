interface Properties extends React.HTMLProps<HTMLInputElement> {
	scale?: number
}

function Icon({ children, scale = 1, ...props }: Properties): JSX.Element {
	return (
		<span
			className='inline-block'
			style={{ transform: `scale(${scale})` }}
			{...props}
		>
			{children}
		</span>
	)
}

export default Icon
