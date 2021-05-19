from pydantic import BaseModel, Field
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union
)


class NonRevoked(BaseModel):
    to: int = Field(
        1621431938
    )


class Restriction(BaseModel):
    cred_def_id: str = Field(
        "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",

    )
    issuer_did: str = Field(
        "WgWxqztrNooG92RXvxSTWv"
    )
    schema_id: str = Field(
        "WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0"
    )
    schema_issuer_did: str = Field(
        "WgWxqztrNooG92RXvxSTWv"
    )
    schema_name: str = Field(
        "transcript"
    )
    schema_version: str = Field(
        "1.0"
    )

class Attribute(BaseModel):
    name: str = Field(
        "Job Title",
        title="Attribute Name"
    )
    non_revoked: NonRevoked
    names: List[str]
    restrictions: List[Restriction]

class PredicateAttribute(Attribute):
    p_type: str = Field(">=")
    p_value: int



class RequestedAttributes(BaseModel):
    attributeProperty1: Attribute
    attributeProperty2: Attribute
    attributeProperty3: Attribute

class RequestedPredicates(BaseModel):
    predicatedAttributeProperty1: PredicateAttribute
    predicatedAttributeProperty2: PredicateAttribute



class ProofRequest(BaseModel):
    name: str = Field(
        "ODIC Proof Name",
        description="Name of proof request"
    )
    version: str
    requested_attributes: RequestedAttributes = Field(
        title="Requested Attributes",
        description="The set of attributes you will challenge users to present"
    )
    requested_predicates: RequestedPredicates = Field(
        description="Requested predicate proofs of attribute values"
    )

class OIDCProofRequest(BaseModel):
    oidc_scope: str
    subject_identifier: str
    proof_request: ProofRequest