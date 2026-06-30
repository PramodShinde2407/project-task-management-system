from sqlalchemy import create_engine
from ..core.config import settings
DATABASE_URL=settings.DATABASE_URL

engine=create_engine(DATABASE_URL)