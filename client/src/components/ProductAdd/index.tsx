import Button from 'components/_atoms/Button'
import Field from 'components/_atoms/Field'
import { useState } from 'react'
import { useForm } from 'react-hook-form'

enum STEPS {
	FIRST,
	SECOND,
	THIRD
}

function ProductAdd(): JSX.Element {
	const [step, setStep] = useState<STEPS>(STEPS.FIRST)
	const { register, handleSubmit } = useForm()

	return (
		<form onSubmit={handleSubmit(data => console.log(data))}>
			{step === STEPS.FIRST && (
				<>
					<Field name='url' label='Url' register={register} />
					<Field
						name='threshold_price'
						label='Threshold price'
						register={register}
					/>
					<div className='mt-5'>
						<Button onClick={() => setStep(STEPS.SECOND)}>Confirm</Button>
					</div>
				</>
			)}
			{step === STEPS.SECOND && (
				<>
					<Field name='email' label='Email' register={register} />
					<div className='mt-5'>
						<Button onClick={() => setStep(STEPS.THIRD)}>Confirm</Button>
					</div>
				</>
			)}
			{step === STEPS.THIRD && (
				<>
					<Field name='code' label='Code' register={register} />
					<div className='mt-5'>
						<Button type='submit'>Submit</Button>
					</div>
				</>
			)}
		</form>
	)
}

export default ProductAdd
