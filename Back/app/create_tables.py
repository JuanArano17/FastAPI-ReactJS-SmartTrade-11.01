from app.base import Base
from app.database import get_engine

engine = get_engine()
Base.metadata.create_all(bind=engine)
