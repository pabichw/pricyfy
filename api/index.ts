import dotenv from 'dotenv';
import app from './__app';
import initRoutes from './routes';

dotenv.config();

const port = process.env.PORT;

initRoutes();

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at ${port}`);
});