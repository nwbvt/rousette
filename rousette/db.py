from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine

METADATA = MetaData()

MODEL = Table("model", METADATA,
    Column("model_id", Integer, primary_key=True),
    Column("num_features", Integer),
    Column("defintion_location", String))


def get_db(config):
    """
    Get a database connection
    """
    conn_string = config["DB"]["CONNECTION_STRING"]
    conn_params = config["DB"].get("CONN_PARAMS")
    optional_args = config["DB"].get("ARGS", {})
    return create_engine(conn_string.format(**conn_params), **optional_args)


def init_db(config):
    """
    Initialize the database
    """
    with get_db(config).connect() as conn:
        METADATA.create_all(conn)
