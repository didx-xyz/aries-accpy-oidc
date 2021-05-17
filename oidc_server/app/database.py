from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from models import OIDCProofRequest, User


# TODO: Extract into ENV Vars
DATABASE_URL = "postgresql://OIDC_DB_USER:OIDC_PASSWORD@oidc-server-db:5432/OIDC"

engine = create_engine(
    DATABASE_URL
)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)