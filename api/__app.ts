import express, { Express } from 'express';

let app: Express | null  = null;

const _getApp = (): Express => {
    if (app) {
        return app
    } else {
        app = express()
        return app
    }
}

export default _getApp()