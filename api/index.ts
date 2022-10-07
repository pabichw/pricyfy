import dotenv from 'dotenv';
import app from './__app';
import initRoutes from './routes';

dotenv.config();

const port = process.env.PORT;

initRoutes();

app.use(function(_, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
  next();
});

app.listen(port, () => {
  console.log(`⚡️[server]: Server is running at ${port}`);
});