import dotenv from 'dotenv';
import app from './__app';
import initRoutes from './routes';
import cors from 'cors'

dotenv.config();

const port = process.env.PORT;

app.use(
  cors({ origin: ['http://127.0.0.1:5173', 'http://localhost:5173', 'https://pricyfy.pabich.cc'] })
)

initRoutes();

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at ${port}`);
});