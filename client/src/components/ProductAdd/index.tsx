import postProductWatch from 'api/postProduct'
import Button from 'components/_atoms/Button'
import Field from 'components/_atoms/Field'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import toast  from 'react-hot-toast'

interface TForm { url: string, threshold_price: string, code: string, email: string }

enum STEPS {
	FIRST,
	SECOND,
	THIRD
}

// eslint-disable-next-line @typescript-eslint/no-magic-numbers
const SUCCESS_HTTP_CODES = new Set([200, 201]);

const notifyAdded = (): void => { toast.success('Added successfully!') }
const notifyError = (message: string): void => { toast.error(`Error: ${message}`) };

const showNotification = (data: { status: number, error: { msg: string } }): void => {
	// TODO: move to global request 'interceptor' 
	if (SUCCESS_HTTP_CODES.has(data.status)) {
		notifyAdded();
	} else {
		notifyError(data.error.msg)
	}
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
		})
		.then(showNotification)
		.finally(() => setIsLoading(false))
	}

	return (
		<form
			// eslint-disable-next-line @typescript-eslint/no-misused-promises
			onSubmit={handleSubmit(onSubmit)}
		>
			{step === STEPS.FIRST && (
				<>
					<fieldset className='united-borders'>
						<Field name='url' label='Url' register={register} />
						<Field
							name='threshold_price'
							label='Threshold price'
							register={register}
						/>
					</fieldset>
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
