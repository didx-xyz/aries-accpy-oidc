from fastapi import APIRouter, HTTPException, Request, Response, Form, status
import logging
from database import session
from models import OIDCProofRequest
from schemas import ProofRequest

router = APIRouter(
    prefix="/oidc/admin/vc-configs",
    tags=["OIDC Proof Request Configuration"],
    responses={404: {"description": "Not found"}},
)


LOGGER = logging.getLogger(__name__)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def vc_configs(request: Request, response: Response):
    oidc_proof_request = session.query(OIDCProofRequest).all()
    LOGGER.info("OIDC Proof Requests Currently Configured:\n", oidc_proof_request)
    return oidc_proof_request
    # return {"hello":"World"}


@router.post(
    "/",
)
async def vc_configs(
    request: Request,
    response: Response,
    oidc_scope: str,
    subject_identifier: str,
    proof_request: ProofRequest,
):
    oidc_proof_request = OIDCProofRequest(oidc_scope=oidc_scope, subject_identifier=subject_identifier,
                                                     proof_request=proof_request)
    LOGGER.info('OIDC Proof Request Added ', oidc_proof_request)
    session.add(oidc_proof_request)
    session.commit()
    return oidc_proof_request


@router.put(
    "/", status_code=204
)
# TODO - Fix Update API for Presentation Configurations. Not working at the moment.
async def vc_configs(
    request: Request,
    response: Response,
    oidc_scope: str,
    subject_identifier: str,
    proof_request: dict,
):
    oidc_proof_request_record = session.query(OIDCProofRequest).filter(OIDCProofRequest.oidc_scope == oidc_scope)

    if not oidc_proof_request_record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"OIDC Proof Request with scope {oidc_scope} not found")

    updated_oidc_pr = OIDCProofRequest(oidc_scope=oidc_scope, subject_identifier=subject_identifier,
                                                     proof_request=proof_request)
    ## TODO revisit log
    LOGGER.info('OIDC Proof Request Updating ', request.body().__str__(), request.headers, request.query_params)
    oidc_proof_request_record.update(updated_oidc_pr)
    session.commit()
    return


@router.delete(
    "/", status_code=204
)
async def vc_configs(request: Request, response: Response, oidc_scope: str):
    oidc_proof_request_record = session.query(OIDCProofRequest).filter(OIDCProofRequest.oidc_scope == oidc_scope)

    if not oidc_proof_request_record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"OIDC Proof Request with scope {oidc_scope} not found")

    oidc_proof_request_record.delete(synchronize_session=False)
    session.commit()
    return
