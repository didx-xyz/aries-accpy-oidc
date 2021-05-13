from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



@router.get('/api/vc-configs/', status_code=status.HTTP_200_OK, tags=['Verifiable Credential Presentation Configuration'])
async def vc_configs(request: Request, response: Response):
    presentation_configuration = db.query(PresentationConfigurations).all()
    print('presentation_configuration ', presentation_configuration)
    return presentation_configuration

@router.post('/api/vc-configs/', tags=['Verifiable Credential Presentation Configuration'])
async def vc_configs(request: Request, response: Response, id: str = Form(...),
        subject_identifier: str = Form(...),
        configuration: str = Form(...)):
    presentation_config = PresentationConfigurations(id=id, subject_identifier=subject_identifier,
                                                     configuration=configuration)
    print('presentation_config ',presentation_config)
    db.add(presentation_config)
    db.commit()
    return presentation_config

@router.put('/api/vc-configs/', tags=['Verifiable Credential Presentation Configuration'])
# TODO - Fix Update API for Presentation Configurations. Not working at the moment.
async def vc_configs(request: Request, response: Response, id: str = Form(...),
        subject_identifier: str = Form(...),
        configuration: str = Form(...)):
    presentation_config_record = db.query(PresentationConfigurations).filter(PresentationConfigurations.id == id)

    if not presentation_config_record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Presentation Config with id {id} not found")

    presentation_config = PresentationConfigurations(id=id, subject_identifier=subject_identifier,
                                                     configuration=configuration)
    print('DEBUG ', request.body().__str__(), request.headers, request.query_params)
    presentation_config_record.update(request)
    db.commit()
    return 'updated'

@router.delete('/api/vc-configs/', tags=['Verifiable Credential Presentation Configuration'])
async def vc_configs(request: Request, response: Response, id: str = Form(...)):
    presentation_config = db.query(PresentationConfigurations).filter(PresentationConfigurations.id == id)

    if not presentation_config.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Presentation Config with id {id} not found")

    presentation_config.delete(synchronize_session=False)
    db.commit()
    return 'done'