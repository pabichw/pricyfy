import express, { Express } from 'express';
import cors from 'cors';

let app: Express | null  = null;

const _getApp = (): Express => {
    if (app) {
        return app
    } else {
        app = express()

        app.use(cors({
            origin: 'https://pricyfy.pabich.cc',
            methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
            allowedHeaders: ['Content-Type', 'Authorization'],
            credentials: true
        }));
        
        return app
    }
}

export default _getApp()