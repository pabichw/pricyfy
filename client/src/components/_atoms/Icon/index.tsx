interface Properties extends React.HTMLProps<HTMLInputElement> {
	height?: number
	width?: number
}

function Icon({
	children,
	height = 24,
	width = 24,
	...props
}: Properties): JSX.Element {
	return (
		<span style={{ height, width }} {...props}>
			{children}
		</span>
	)
}

export default Icon
