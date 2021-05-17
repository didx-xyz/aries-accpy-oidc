'''OIDC server example'''
# import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.sqlite import JSON
# from authlib.integrations.sqla_oauth2 import (
#     OAuth2ClientMixin,
#     OAuth2TokenMixin,
#     OAuth2AuthorizationCodeMixin
# )
from database import Base
from utils import disambiguate_referent


import uuid


class User(Base):  # pylint: disable=R0903
    '''User class example'''

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(100), unique=True)

    def get_id(self):
        '''Fetch user identifier'''
        return self.id


# OIDC Authentication Challenge
# Template for a proof request that will be sent as a challenge to authenticating users
class OIDCProofRequest(Base):
    '''OIDC Proof Request class example'''

    __tablename__ = 'oidc_proof_request'

    # The oidc scope allows a relying party to specify the proof request the OP should challenge the user with
    oidc_scope = Column(String(100), primary_key=True)

    # Attribute within the proof request that identifies the subject responding the to authentication challenge
    subject_identifier = Column(String(100))
    proof_request = Column(JSON)

    def get_oidc_scope(self):
        '''Fetch oidc proof request identifier'''
        return self.oidc_scope

    def __str__(self):
        return f"{self.id}"

    def to_json(self):
        proof_request = {
            "name": self.proof_request.get("name", ""),
            "version": self.proof_request.get("version", ""),
            "requested_attributes": {},
            "requested_predicates": {},
        }

        for attr in self.proof_request.get("requested_attributes", []):
            label = attr.get("label", str(uuid.uuid4()))
            if label in proof_request.get("requested_attributes", {}).keys():
                label = disambiguate_referent(label)
            proof_request["requested_attributes"].update({label: attr})

        for attr in self.proof_request.get("requested_predicates", []):
            label = attr.get("label", str(uuid.uuid4()))
            if label in proof_request.get("requested_predicates", {}).keys():
                label = disambiguate_referent(label)

            proof_request["requested_predicates"].update({label: attr})

        return {"proof_request": proof_request}