import db from '../db';
import { Token } from '../models/Token';

export const validateToken = async (token: Token): Promise<{ status: boolean, error?: string }> => {
    const tokensCollection = db.collection('tokens')
    const tokens = await tokensCollection.find({ id: token.id }).toArray()

    if (tokens.length === 0) {
        return { status: false, error: 'Token not found' }
    } 

    if (tokens.length > 1) {
        return { status: false, error: 'More than one token found' }
    }

    return { status: true };
}