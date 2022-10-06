### Pricify API

#### Prerequirements

- node (v16.14.0)
- npm (8.3.1)

#### Install

`npm i`

#### Dev

`npm run dev`

#### Build

`npm run build`

#### Env

Example `.env` file

```
DATABASE_URL='mongodb://<user>:<pass>@localhost/pricify'
DATABASE_NAME='pricify'
```

#### Database

##### Tokens collection

Tokens let you access certain resources and actions.
To add a valid token add document to `tokens` collection. It should look like the following:

```
{ id: "ABCDEFGHILJKMNO12312312" }
```

Tokens are required in order to access the following routes:

- history
- products (soon)

#### TODOS

- extract token validation to `app.use`
- tests
- do not add to queue already added products
- handle missing params on `/products/watch` endpoint (and other endpoints as well)
