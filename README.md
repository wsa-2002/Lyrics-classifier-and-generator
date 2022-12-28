# Backend

```shell
cd ./backend
conda create --name backend python=3.9
conda activate backend
pip install -r requirements.txt
cp .env.example .env
```

Paste environment variables, download static files
from [this link](https://drive.google.com/file/d/1aj02J33QfypAq14BpsJDGmEF75B6xZKr/view?usp=share_link) and put them in
to `data` folder, then run

```shell
uvicorn main:app --reload
```

or you may just run `docker-compose up` to start backend in the docker container.

Go to `localhost:8000/docs` and you will see backend swagger.

# Frontend

```shell
cd ./frontend
yarn
yarn dev
```

Go to `localhost:5173/` and you will see frontend app.