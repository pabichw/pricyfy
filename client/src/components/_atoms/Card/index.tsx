interface Properties {
	children: React.ReactNode
  noSpacing: boolean
}

function Card({ children, noSpacing }: Properties): JSX.Element {
	return (
		<div
			className={`space-y-px overflow-hidden rounded-md bg-white ${noSpacing ? ``: `px-3 py-4`} shadow-md`}
		>
			{children}
		</div>
	)
}

export default Card
