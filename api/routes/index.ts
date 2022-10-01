import { Response } from 'express';
import app from '../__app';
import initProducts from './products'
import initHistory from './history'

const initRoot = (): void => {
    app.get('/', async (_, res: Response): Promise<void> => {
        res.send('Nic tu nie ma. ⚠️');
    });
      
}
export default (): void => {
    initRoot();
    initProducts();
    initHistory();
}