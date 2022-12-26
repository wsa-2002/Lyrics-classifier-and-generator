# Backend

```shell
cd ./backend
conda create --name backend python=3.9
conda activate backend
pip install -r requirements.txt
cp .env.example .env
```

paste environment variables

```shell
pip install uvicorn
uvicorn main:app --reload
```

Go to `localhost:8000/docs` and you will see backend swagger.

# Frontend

```shell
cd ./frontend
yarn
yarn dev
```

Go to `localhost:5173/` and you will see frontend app.