'''OIDC server example'''
# import datetime
import time
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON, BOOLEAN, DATETIME
# from authlib.integrations.sqla_oauth2 import (
#     OAuth2ClientMixin,
#     OAuth2TokenMixin,
#     OAuth2AuthorizationCodeMixin
# )
from app.database import Base, db
from app.utils import disambiguate_referent


import uuid
import os

class User(Base):  # pylint: disable=R0903
    '''User class example'''

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(100), unique=True)

    def get_id(self):
        '''Fetch user identifier'''
        return self.id


# OIDC Authentication Challenge
# Template for a proof request that will be sent as a challenge to authenticating users
class OIDCProofRequest(Base):
    '''Presentation Configuration class example'''

    __tablename__ = 'oidc_proof_request'

    id = Column(String(100), primary_key=True)
    # The oidc scope
    oidc_scope_identifier = Column(String(100))
    proof_request = Column(JSON)

    def get_id(self):
        '''Fetch oidc proof request identifier'''
        return self.id

    def __str__(self):
        return f"{self.id}"

    def to_json(self):
        proof_request = {
            "name": self.configuration.get("name", ""),
            "version": self.configuration.get("version", ""),
            "requested_attributes": {},
            "requested_predicates": {},
        }

        for attr in self.configuration.get("requested_attributes", []):
            label = attr.get("label", str(uuid.uuid4()))
            if label in proof_request.get("requested_attributes", {}).keys():
                label = disambiguate_referent(label)
            proof_request["requested_attributes"].update({label: attr})

        for attr in self.configuration.get("requested_predicates", []):
            label = attr.get("label", str(uuid.uuid4()))
            if label in proof_request.get("requested_predicates", {}).keys():
                label = disambiguate_referent(label)

            proof_request["requested_predicates"].update({label: attr})

        return {"proof_request": proof_request}