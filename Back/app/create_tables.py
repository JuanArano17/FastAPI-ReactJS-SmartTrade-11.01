from database import Base, get_engine_from_settings

# does not wipe the contents of the tables
engine = get_engine_from_settings()
Base.metadata.create_all(bind=engine)
