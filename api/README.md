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

For production envieronment pass these variables via `flyctl` as follows:

```
flyctl secrets set DATABASE_URL=mongodb://<user>:<pass>@<address>:<port>/<database_name> DATABASE_NAME=ABCDEF
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

#### DEPLOY
Platform: `fly.io`
To deploy run `fly deploy`

Prod database available at `moa.mydevil.net`.

#### TODOS

- extract token validation to `app.use`
- tests
- do not add to queue already added products
- handle missing params on `/products/watch` endpoint (and other endpoints as well)


