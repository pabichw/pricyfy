import React from 'react'
import { format, parse, parseISO } from 'date-fns'
import TrendGrowingIcon from 'components/__icons/TrendGrowingIcon';
import TrendDivingIcon from 'components/__icons/TrendDivingIcon';
import type { StatisticsDTO } from 'types/types'
import type { ReactElement } from 'react'


interface StatsShowcaseProperties {
  stats: StatisticsDTO[]
}

export default function StatsShowcase({ stats }: StatsShowcaseProperties) {
  if (!stats) {
    return null;
  }

  const nameMapper = {
    'count': 'Products monitored',
    'average_change': 'Average change',
    'works_since': 'Monitoring since'
  }

  const valuePrepare = (name: string, value: string): { value: string, icon?: ReactElement, style?: string } => { // TODO: can be (name: Keys of StatisticsDTO, value: values of StatisticsDTO)
    switch (name) {
      case 'average_change':
        return ({
          value: `${value} zł`,
          icon: Number(value) < 0 ? <TrendDivingIcon /> : <TrendGrowingIcon />,
          style: Number(value) < 0 ? `value-better text-lime-600` : 'value-worse text-red-600',
        })
      case 'works_since':
        return ({
          value: format(parseISO(value), 'dd MMMM yyyy')
        })
      default:
        return ({ value })
    }
  }

  return (
    <div className='flex flex-col md:flex-row justify-center gap-5'>
      {Object.entries(stats)
        .filter(([name]) => !['_id', 'created_at'].includes(name))
        .map(([name, value]) => {
          const preparedValue = valuePrepare(name, value)

          return (
            <div className='flex flex-col align-center justify-center w-100 md:w-56 py-16 bg-white rounded-md shadow-md '>
              <span className='block text-m text-slate-700 text-center'>{nameMapper[name]}</span>
              <span className={`mt-1 flex items-center justify-center text-xl text-center font-bold ${preparedValue.style}`}>
                {preparedValue.icon &&
                  <span className='mr-2'>
                    {preparedValue.icon}
                  </span>
                }
                {preparedValue.value}
              </span>
            </div>
          )
        })
      }
    </div>
  )
}
