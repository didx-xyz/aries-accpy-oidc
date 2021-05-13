from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: Extract into ENV Vars
DATABASE_URL = "postgres://OIDC_DB_USER:OIDC_PASSWORD@oidc-server-db:5432"

db = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)

Base = declarative_base()


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

