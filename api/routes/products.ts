import { Request, Response } from 'express'
import bodyParser from 'body-parser';
import app from '../__app';
import db from '../db';
import { validateToken } from '../utils/tokens';
import { Token } from '../models/Token';
import pick from 'lodash/pick';
import { Product, ProductQueueEntry, ProductStatus } from '../types/types';

const jsonParser = bodyParser.json()

export default (): void => {
    app.get('/products', async (req: Request, res: Response): Promise<void> => {
        const productsCollection = db.collection('products')
        const product = await productsCollection.find({ product_id: req.query.id }).toArray()

        res.send({ status: 200, data: { product }});
    });

    app.get('/products/recent', async (req: Request, res: Response): Promise<void> => {
        const productsCollection = db.collection<Product>('products')
        const products = await productsCollection.find({}).sort({ $natural: -1}).limit(10).toArray()

        const fields = ['_id', 'images', 'last_found_price', 'product_id', 'status', 'url']
        const noJustAdded = (product: Product) => product.status !== ProductStatus.JUST_ADDED

        res.send({ status: 200, data: { products: products.filter(noJustAdded).map(product => pick(product, fields)) }})
    })

    app.post('/products/watch', jsonParser, async (req: Request<{}, {}, {url: string, threshold_price: string, token: string, email: string}>, res: Response): Promise<void> => {
        const { body } = req;

        const token: Token = { id: body.token }
        const validationResult = await validateToken(token);

        if (!validationResult.status) {
            res.status(401);
            res.send({ status: 401, error: { msg: 'Unauthorized' }});
            return;
        }

        const productsCollection = db.collection<ProductQueueEntry>('products_queue')
        const findResult = await productsCollection.countDocuments({ 'url': body.url }, { limit: 1 });
        
        if (findResult > 0) {
            await productsCollection.updateOne({ url: body.url }, { $addToSet: { recipients: body.email }})
        } else {
            const insertResult = await productsCollection.insertOne({ 
                url: body.url, 
                threshold_price: Number(body.threshold_price),
                recipients: [body.email]
            })
    
            if (insertResult) {
                console.log(`[Queue] Product added: ${body.url} : ${body.threshold_price}`)
            }
        }

        res.send({ status: 200, data: { msg: 'OK' }});
    });
}