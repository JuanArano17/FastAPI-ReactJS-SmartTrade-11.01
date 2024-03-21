from app.database import Base, get_engine

# does not wipe the contents of the tables
engine = get_engine()
Base.metadata.create_all(bind=engine)
