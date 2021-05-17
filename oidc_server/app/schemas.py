from pydantic import BaseModel, Field


class Attribute(BaseModel):
    name: str
    non_revoked: str


class RequestedAttributes(BaseModel):
    attribute: Attribute


class ProofRequest(BaseModel):
    name: str
    version: str
    requested_attributes: RequestedAttributes = Field(
        title="Requested Attributes",
        description="The set of attributes you will challenge users to present"
    )
