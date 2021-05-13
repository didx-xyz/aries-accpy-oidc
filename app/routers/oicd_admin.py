from fastapi import APIRouter, HTTPException, Request, Response, Form, status
import logging
from ..database import db
from ..models import OIDCProofRequest

router = APIRouter()


LOGGER = logging.getLogger(__name__)


@router.get(
    "/oidc/admin/vc-configs/",
    status_code=status.HTTP_200_OK,
    tags=["Verifiable Credential Presentation Configuration"],
)
async def vc_configs(request: Request, response: Response):
    oidc_proof_request = db.query(OIDCProofRequest).all()
    LOGGER.info("OIDC Proof Requests Currently Configured:\n", oidc_proof_request)
    return oidc_proof_request


@router.post(
    "/oidc/admin/vc-configs/", tags=["Verifiable Credential Presentation Configuration"]
)
async def vc_configs(
    request: Request,
    response: Response,
    oidc_scope: str,
    subject_identifier: str,
    proof_request: dict,
):
    oidc_proof_request = OIDCProofRequest(oidc_scope=oidc_scope, subject_identifier=subject_identifier,
                                                     proof_request=proof_request)
    LOGGER.info('OIDC Proof Request Added ', oidc_proof_request)
    db.add(oidc_proof_request)
    db.commit()
    return oidc_proof_request


@router.put(
    "/oidc/admin/vc-configs/", tags=["Verifiable Credential Presentation Configuration"]
)
# TODO - Fix Update API for Presentation Configurations. Not working at the moment.
async def vc_configs(
    request: Request,
    response: Response,
    id: str = Form(...),
    subject_identifier: str = Form(...),
    configuration: str = Form(...),
):
    pass


@router.delete(
    "/oidc/admin/vc-configs/", tags=["Verifiable Credential Presentation Configuration"]
)
async def vc_configs(request: Request, response: Response, id: str = Form(...)):
    pass
