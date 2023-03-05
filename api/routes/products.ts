import { Request, Response } from 'express'
import bodyParser from 'body-parser';
import app from '../__app';
import db from '../db';
import { validateToken } from '../utils/tokens';
import { Token } from '../models/Token';
import pick from 'lodash/pick';
import { HistoryEntry, Product, ProductQueueEntry, ProductStatus } from '../types/types';
import { Document } from 'mongodb';

const jsonParser = bodyParser.json()

export default (): void => {
    app.get('/products', async (req: Request, res: Response): Promise<void> => {
        const productsCollection = db.collection('products')
        let products

        if (req.query.id) {
            products = await productsCollection.find({ product_id: req.query.id }).toArray()
        } else {
            products = await productsCollection.find({}).toArray()
        }

        res.send({ status: 200, data: { products }});
    });

    app.get('/products/recent', async (_, res: Response): Promise<void> => {
        const fields = ['_id', 'price_history', 'images', 'last_found_price', 'product_id', 'status', 'url']

        const productsCollection = db.collection<Product>('products')
        const products = (await productsCollection.aggregate([
            { $match: { status: { $ne: ProductStatus.JUST_ADDED }}},
            { $lookup: {
                from: 'history',
                localField: 'product_id',
                foreignField: 'product_id',
                as: 'price_history'
                }
            },
            { $sort: { _id: -1 } },
            { $limit: 15 }
        ])
        .toArray())
        .map((product: Document) => ({...pick(product, fields) }))

        res.send({ status: 200, data: { products }})
    })

    app.post('/products/watch', jsonParser, async (req: Request<{}, {}, {url: string, token: string, email: string}>, res: Response): Promise<void> => {
        const { body } = req;

        const token: Token = { id: body.token }
        const validationResult = await validateToken(token);

        if (!validationResult.status) {
            res.status(401);
            res.send({ status: 401, error: { msg: 'Unauthorized' }});
            return;
        }

        const productsCollection = db.collection<ProductQueueEntry>('products_queue')
        const count = await productsCollection.countDocuments({ 'url': body.url }, { limit: 1 });
        
        if (count > 0) {
            await productsCollection.updateOne({ url: body.url }, { $addToSet: { recipients: body.email }})
        } else {
            const insertResult = await productsCollection.insertOne({ 
                url: body.url, 
                recipients: [body.email]
            })
    
            if (insertResult) {
                console.log(`[Queue] Product added: ${body.url}`)
            }
        }

        res.send({ status: 200, data: { msg: 'OK' }});
    });

    app.get('/products/:id/history', async (req: Request<{id: string}>, res: Response): Promise<void> => {
        const historyCollection = db.collection<HistoryEntry>('history')
        const history = await historyCollection.find({'product_id': req.params.id}).sort({ $natural: -1}).limit(10).toArray()

        const fields = ['parse_time', 'price_parsed']
        res.send({ status: 200, data: { history: history.map(hist => pick(hist, fields)) }}) 
    })
}
