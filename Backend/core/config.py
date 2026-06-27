from fastapi import os



DATABASE_URL=os.getenv("DATABASE_URL")
SECRETE_KEY=os.getenv("SECRETE_KEY")
ACCESS_TOKEN_EXPIRE_TIME=int(os.getenv("ACCESS_TOKEN_EXPIRE_TIME"))