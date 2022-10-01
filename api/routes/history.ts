import { Request, Response } from 'express'
import app from '../__app';
import db from '../db';

export default (): void => {
    app.get('/history', async (req: Request, res: Response): Promise<void> => {
        const historyCollection = db.collection('history')
        const history = await historyCollection.find({ product_id: req.query.id }).toArray()
        
        res.send({ status: 200, data: { history }});
    });
}