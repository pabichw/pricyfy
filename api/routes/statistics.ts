import { Response } from 'express'
import app from '../__app';
import db from '../db';
import { StatisticsEntry } from '../types/types';

export default (): void => {
  app.get('/statistics/last', async (_, res: Response): Promise<void> => {
    const statisticsCollection = db.collection<StatisticsEntry>('statistics')
    const lastStatistics = await statisticsCollection.find().sort([['_id', -1]]).limit(1).next()

    res.send({ status: 200, data: { statistics: lastStatistics } })
  })
}
