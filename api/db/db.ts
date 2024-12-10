import { MongoClient } from 'mongodb'
import dotenv from 'dotenv';

dotenv.config();

console.log(process.env.DATABASE_URL);
const _instance = new MongoClient(process.env.DATABASE_URL || '')

export default _instance.db(process.env.DATABASE_NAME)
