import { Request, Response } from 'express'
import app from '../__app';
import db from '../db';
import { validateToken } from '../utils/tokens';
import { Token } from '../models/Token';

export default (): void => {
    app.get('/products', async (req: Request, res: Response): Promise<void> => {
        const productsCollection = db.collection('products')
        const product = await productsCollection.find({ product_id: req.query.id }).toArray()

        res.send({ status: 200, data: { product }});
    });

    app.post('/products/watch', async (req: Request<{}, {}, {}, {url: string, threshold_price: string, token: string}>, res: Response): Promise<void> => {
        const token: Token = { id: req.query.token }
        const validationResult = await validateToken(token);
        if (!validationResult.status) {
            res.send({ status: 401, error: { msg: 'Unauthorized' }});
            return;
        }

        const { query } = req;
        const productsCollection = db.collection('products_queue')
        const result = await productsCollection.insertOne({ url: query.url, threshold_price: query.threshold_price })

        if (result) {
            console.log(`[Queue] Product added: ${query.url} : ${query.threshold_price}`)
        }

        res.send({ status: 200, data: { msg: 'OK' }});
    });
}