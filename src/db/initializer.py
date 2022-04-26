from sqlalchemy import create_engine



# Create Engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
