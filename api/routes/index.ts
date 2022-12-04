import { Response } from 'express';
import app from '../__app';
import initProducts from './products'
import initHistory from './history'
import initStatistics from './statistics'

const initRoot = (): void => {
    app.get('/', async (_, res: Response): Promise<void> => {
        res.send('Nie ma tu nic ⚠️');
    });
}

const initTest = (): void => {
    app.get('/marco', async (_, res: Response): Promise<void> => {
        res.send({ status: 200, data: { msg: 'polo' }});
    });
}

export default (): void => {
    initRoot();
    initTest();
    initProducts();
    initHistory();
    initStatistics();
}