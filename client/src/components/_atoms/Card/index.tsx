interface Properties {
	children: React.ReactNode
}

function Card({ children }: Properties): JSX.Element {
	return (
		<div
			className='my-12 -space-y-px rounded-md bg-white px-3 py-4 shadow-md'
		>
			{children}
		</div>
	)
}

export default Card
