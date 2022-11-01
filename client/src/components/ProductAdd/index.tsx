import postProductWatch from 'api/postProduct'
import Button from 'components/_atoms/Button'
import Field from 'components/_atoms/Field'
import Icon from 'components/_atoms/Icon'
import Check from 'components/__icons/Check/index'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'

interface TForm {
	url: string
	threshold_price: string
	code: string
	email: string
}

enum STEPS {
	FIRST,
	SECOND,
	THIRD,
	FOURTH
}

// eslint-disable-next-line @typescript-eslint/no-magic-numbers
const SUCCESS_HTTP_CODES = new Set([200, 201])

const notifyError = (message: string): void => {
	toast.error(`Error: ${message}`)
}

function ProductAdd(): JSX.Element {
	const [isLoading, setIsLoading] = useState<boolean>(false)
	const [step, setStep] = useState<STEPS>(STEPS.FOURTH)

	const { register, handleSubmit } = useForm<TForm>()

	const handleResponse = (data: {
		status: number
		error: { msg: string }
	}): void => {
		// TODO: move to global request 'interceptor'
		if (SUCCESS_HTTP_CODES.has(data.status)) {
			setStep(STEPS.FOURTH)
		} else {
			notifyError(data.error.msg)
		}
	}

	const onSubmit = async (data: TForm): Promise<void> => {
		setIsLoading(true)
		await postProductWatch({
			url: data.url,
			threshold_price: data.threshold_price,
			token: data.code,
			email: data.email
		})
			.then(handleResponse)
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
					<Field
						name='email'
						label='Email'
						type='email'
						required
						register={register}
					/>
					<div className='mt-5'>
						<Button onClick={(): void => setStep(STEPS.THIRD)}>Confirm</Button>
					</div>
				</>
			)}
			{step === STEPS.THIRD && (
				<>
					<Field name='code' label='code' register={register} />
					<div className='mt-5'>
						<Button type='submit'>{isLoading ? 'loading...' : 'submit'}</Button>
					</div>
				</>
			)}
			{step === STEPS.FOURTH && (
				<>
					<Icon>
						<Check />
					</Icon>
					<p className='text-m mt-1 text-center font-bold text-gray-900'>
						All done
					</p>
					<div className='mt-5'>
						<Button onClick={() => setStep(STEPS.FIRST)}>Add another</Button>
					</div>
				</>
			)}
		</form>
	)
}

export default ProductAdd
