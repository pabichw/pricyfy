import postProductWatch from 'api/postProduct'
import Button from 'components/_atoms/Button'
import Field from 'components/_atoms/Field'
import { useState } from 'react'
import { useForm } from 'react-hook-form'

interface TForm { url: string, threshold_price: string, code: string, email: string }

enum STEPS {
	FIRST,
	SECOND,
	THIRD
}

function ProductAdd(): JSX.Element {
	const [isLoading, setIsLoading] = useState<boolean>(false);
	const [step, setStep] = useState<STEPS>(STEPS.FIRST)

	const { register, handleSubmit } = useForm<TForm>()

	const onSubmit = async (data: TForm): Promise<void> => {
		setIsLoading(true)
		await postProductWatch({
			url: data.url,
			threshold_price: data.threshold_price,
			token: data.code,
			email: data.email
		}).finally(() => setIsLoading(false))
	}

	return (
		<form
			// eslint-disable-next-line @typescript-eslint/no-misused-promises
			onSubmit={handleSubmit(onSubmit)}
		>
			{step === STEPS.FIRST && (
				<>
					<Field name='url' label='Url' register={register} />
					<Field
						name='threshold_price'
						label='Threshold price'
						register={register}
					/>
					<div className='mt-5'>
						<Button onClick={(): void => setStep(STEPS.SECOND)}>Confirm</Button>
					</div>
				</>
			)}
			{step === STEPS.SECOND && (
				<>
					<Field name='email' label='Email' type='email' required register={register} />
					<div className='mt-5'>
						<Button onClick={(): void => setStep(STEPS.THIRD)}>Confirm</Button>
					</div>
				</>
			)}
			{step === STEPS.THIRD && (
				<>
					<Field name='code' label='Code' register={register} />
					<div className='mt-5'>
						<Button type='submit'>{ isLoading? 'Loading...' : 'Submit' }</Button>
					</div>
				</>
			)}
		</form>
	)
}

export default ProductAdd
