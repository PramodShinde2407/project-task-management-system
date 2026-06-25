from sqlalchemy.orm import sessionmaker
from .connection import engine
SessionLoad=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db=SessionLoad()
    try:
        yield db
    finally:
        db.close()