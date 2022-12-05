```shell
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

go to localhost:8000/docs and you will see backend swagger
