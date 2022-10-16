import { Request, Response } from 'express'
import app from '../__app';
import db from '../db';
import { validateToken } from '../utils/tokens';
import { Token } from '../models/Token';

export default (): void => {
    app.get('/history', async (req: Request<{}, {}, {}, { token: string, id: string }>, res: Response): Promise<void> => {
        const token: Token = { id: req.query.token }
        const validationResult = await validateToken(token);
        if (!validationResult.status) {
            res.status(401);
            res.send({ status: 401, error: { msg: 'Unauthorized' }});
            return;
        }
        
        const historyCollection = db.collection('history')
        const history = await historyCollection.find({ product_id: req.query.id }).toArray()
        
        res.send({ status: 200, data: { history }});
    });
}