import { Response, Request } from 'express';
import dotenv from 'dotenv';
import db from './db';
import app from './__app';
import initRoutes from './routes';

dotenv.config();

const port = process.env.PORT;

initRoutes();

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at https://localhost:${port}`);
});