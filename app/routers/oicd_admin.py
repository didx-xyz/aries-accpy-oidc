from fastapi import APIRouter, HTTPException, Request, Response, Form, status
import logging
from ..database import db
from ..models import OIDCProofRequest

router = APIRouter()


LOGGER = logging.getLogger(__name__)


@router.get(
    "/oidc/admin/vc-configs/",
    status_code=status.HTTP_200_OK,
    tags=["OIDC Proof Request Configuration"],
)
async def vc_configs(request: Request, response: Response):
    oidc_proof_request = db.query(OIDCProofRequest).all()
    LOGGER.info("OIDC Proof Requests Currently Configured:\n", oidc_proof_request)
    return oidc_proof_request


@router.post(
    "/oidc/admin/vc-configs/", tags=["OIDC Proof Request Configuration"]
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
    "/oidc/admin/vc-configs/", tags=["OIDC Proof Request Configuration"], status=204
)
# TODO - Fix Update API for Presentation Configurations. Not working at the moment.
async def vc_configs(
    request: Request,
    response: Response,
    oidc_scope: str,
    subject_identifier: str,
    proof_request: str,
):
    oidc_proof_request_record = db.query(OIDCProofRequest).filter(OIDCProofRequest.oidc_scope == oidc_scope)

    if not oidc_proof_request_record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"OIDC Proof Request with scope {oidc_scope} not found")

    updated_oidc_pr = OIDCProofRequest(oidc_scope=oidc_scope, subject_identifier=subject_identifier,
                                                     proof_request=proof_request)
    ## TODO revisit log
    LOGGER.info('OIDC Proof Request Updating ', request.body().__str__(), request.headers, request.query_params)
    oidc_proof_request_record.update(updated_oidc_pr)
    db.commit()
    return


@router.delete(
    "/oidc/admin/vc-configs/", tags=["OIDC Proof Request Configuration"], status=204
)
async def vc_configs(request: Request, response: Response, oidc_scope: str):
    oidc_proof_request_record = db.query(OIDCProofRequest).filter(OIDCProofRequest.oidc_scope == oidc_scope)

    if not oidc_proof_request_record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"OIDC Proof Request with scope {oidc_scope} not found")

    oidc_proof_request_record.delete(synchronize_session=False)
    db.commit()
    return
