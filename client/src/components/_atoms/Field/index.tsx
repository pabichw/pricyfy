import { forwardRef } from 'react'

interface Properties extends React.HTMLProps<HTMLInputElement> {
	label?: string
	register: any // take from react hook form
}

const Field = forwardRef<RTCEncodedVideoFrameType, Properties>(
	({ name, label, register, type, ...rest }): JSX.Element => {
		return (
			<div>
				<label htmlFor={name} className='hidden'>
					{label}
				</label>
				<input
					className='relative block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm'
					type={type}
					placeholder={label}
					{...register(name)}
					{...rest}
				/>
			</div>
		)
	}
)

export default Field
