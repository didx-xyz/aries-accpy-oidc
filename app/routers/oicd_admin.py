from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get(
    "/oidc/admin/vc-configs/",
    status_code=status.HTTP_200_OK,
    tags=["Verifiable Credential Presentation Configuration"],
)
async def vc_configs(request: Request, response: Response):
    pass


@router.post(
    "/oidc/admin/vc-configs/", tags=["Verifiable Credential Presentation Configuration"]
)
async def vc_configs(
    request: Request,
    response: Response,
    id: str = Form(...),
    subject_identifier: str = Form(...),
    configuration: str = Form(...),
):
    pass


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
