import express, { Response, Request } from 'express';
import dotenv from 'dotenv';
import db from './db';

dotenv.config();

const app = express();
const port = process.env.PORT;

app.get('/', (_, res: Response) => {
  res.send('Nic.');
});

app.get('/products', async (req: Request, res: Response) => {
  const productsCollection = db.collection('products')
  const product = await productsCollection.findOne({ product_id: req.query.id })

  res.send({ status: 200, data: { product }});
});

app.get('/history', async (req: Request, res: Response) => {
  const historyCollection = db.collection('history')
  const history = await historyCollection.find({ product_id: req.query.id }).toArray()
  
  res.send({ status: 200, data: { history }});
});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at https://localhost:${port}`);
});