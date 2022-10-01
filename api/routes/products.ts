import { Request, Response } from 'express'
import app from '../__app';
import db from '../db';

export default (): void => {
    app.get('/products', async (req: Request, res: Response): Promise<void> => {
        const productsCollection = db.collection('products')
        const product = await productsCollection.find({ product_id: req.query.id }).toArray()

        res.send({ status: 200, data: { product }});
    });
}