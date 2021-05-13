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


import uuid
import os


class PresentationConfiguration(Base):
    '''Presentation Configuration class example'''

    __tablename__ = 'presentation_configs'

    id = Column(String(100), primary_key=True)
    subject_identifier = Column(String(100))
    configuration = Column(JSON)

    def get_presentation_id(self):
        '''Fetch presentation config identifier'''
        return self.id

    def __str__(self):
        return f"{self.id}"

    def to_json(self):
        presentation_request = {
            "name": self.configuration.get("name", ""),
            "version": self.configuration.get("version", ""),
            "requested_attributes": {},
            "requested_predicates": {},
        }

        for attr in self.configuration.get("requested_attributes", []):
            label = attr.get("label", str(uuid.uuid4()))
            if label in presentation_request.get("requested_attributes", {}).keys():
                label = disambiguate_referent(label)
            presentation_request["requested_attributes"].update({label: attr})

        for attr in self.configuration.get("requested_predicates", []):
            label = attr.get("label", str(uuid.uuid4()))
            if label in presentation_request.get("requested_predicates", {}).keys():
                label = disambiguate_referent(label)

            presentation_request["requested_predicates"].update({label: attr})

        return {"proof_request": presentation_request}