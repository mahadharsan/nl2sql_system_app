from sqlalchemy import create_engine

def connect_database(db_type, user, password, host, port, dbname):
    """
    Connect to any supported database via SQLAlchemy.
    db_type: 'sqlite', 'postgresql', 'mysql', 'mssql', 'oracle', etc.
    """
    if db_type == "sqlite":
        engine = create_engine(f"sqlite:///{dbname}")
    elif db_type == "postgresql":
        engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")
    elif db_type == "mysql":
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}")
    elif db_type == "mssql":
        engine = create_engine(f"mssql+pyodbc://{user}:{password}@{host}/{dbname}?driver=ODBC+Driver+17+for+SQL+Server")
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
    return engine
