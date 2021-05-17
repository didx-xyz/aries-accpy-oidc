from pydantic import BaseModel


class RequestedAttributes(BaseModel):


class ProofRequest(BaseModel):
    name: str
    version: str
    requested_attributes: RequestedAttributes