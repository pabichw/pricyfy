import type { ChartData, ChartOptions, Color, ScriptableContext } from 'chart.js';
import {
  CategoryScale, Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, Title,
  Tooltip,
  Filler,
} from 'chart.js';
import { formatPrice } from 'components/utils/Price';
import { Line } from 'react-chartjs-2';
import type { Product } from 'types/types';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

export const options: ChartOptions<'line'> = {
  elements: {
    point: {
      radius: 2,
    }
  },
  layout: {
    padding: 0
  },
  responsive: true,
  plugins: {
    filler: {
      propagate: false
    },
    legend: {
      display: false
    },
    title: {
      display: false,
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
      ticks: {
        display: false
      }
    },
    y: {
      grid: {
        display: true,
      },
      ticks: {
        display: false
      }
    }
  }
};

interface Properties {
	data: Product
}

function ProductsShowcaseItem({ data }: Properties): JSX.Element {
  const historyData: ChartData<'line'> = { // memoize
    labels: data.price_history.map(hist => hist.parse_time),
    datasets: [
      {
        data: data.price_history.map(hist => Number.parseInt(hist.price_parsed, 10)), 
        borderColor: 'rgba(75,192,192,0.9)',
        backgroundColor: (context: ScriptableContext<"line">): Color => {
          const {chart: { ctx }} = context;
          const gradient = ctx.createLinearGradient(0, 0, 0, 200);
          gradient.addColorStop(0, "rgba(75,192,192,0.2)");
          gradient.addColorStop(1, "rgba(75,192,192,0.9)");
          return gradient;
        },
        fill: true,
      }
    ],
  }

	return (
		<li className='group h-[6rem] rounded-md bg-white p-3 text-gray-800 shadow-md transition hover:shadow-xl'>
			<a
				href={data.url}
				className='grid h-full w-full grid-cols-6 gap-x-2 sm:gap-x-4'
				target='__blank'
				referrerPolicy='no-referrer'
			>
				<span className='col-span-1 mx-auto overflow-hidden'>
					<img
						loading='lazy'
						alt="product thumbnail"
						className='max-h-full'
						src={data.images?.[0]}
					/>
				</span>
				<span className='col-span-2 sm:col-span-3 text-sm line-clamp-3 group-hover:underline'>
					{data.product_id}
				</span>
        <span className='col-span-1'>
          <Line 
            options={options} 
            data={historyData}
          />
        </span>
				<span className='col-span-2 sm:col-span-1 text-right font-bold'>
					{formatPrice(data.last_found_price, { code: 'PLN', symbol: 'zł' })}
				</span>
			</a>
		</li>
	)
}

export default ProductsShowcaseItem
