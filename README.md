# Chat Application

### Dependencies
You can install dependencies using the provided [conda](https://anaconda.org/anaconda/conda) enviroment, `backend/enviroment.yml`.

If you don't want to use a conda env you can install the current dependencies:
```bash
pip install fastapi
pip install psycopg2
pip install jwt
pip install passlib[bcrypt]
pip install bcrypt==4.0.1
```

You will also need to have [PostgreSQL](https://www.postgresql.org/) on your device.

### Running the App

```bash
cd backend
fastapi dev main.py
```

### Backend File Structure

```
├── config
├── controllers
├── models
├── static
└── utils
```

- `config`: interface for enviroment variables. Currently not used but might be useful later.
- `controllers`: defines API routes.
- `models`: DB interface. Normally used to define the DB schemas, but the file in there now also has an interface to use the DB, making it simple and easy to use.
- `static`: frontend files to serve to client.
- `utils`: miscellaneous helpers.

