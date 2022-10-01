type Action = {
    type: 'PRODUCT_WATCH'
    value: any 
}

export type Token = {
    id: string;
    bindedAction?: Action
}