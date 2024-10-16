from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.feature import Feature, Geometry, Properties

router = APIRouter(prefix="/features", tags=["features"])


@router.post("/")
async def create_feature(request: Request, feature: Feature = Body(...)):
    try:
        geo = jsonable_encoder(feature.geometry)
        await request.app.t38.set(feature.properties.key, feature.properties.id).object(geo).exec()
        return JSONResponse(content={"message": "Feature created"}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)


@router.get("/{key}")
async def read_zone(key: str, request: Request):
    try:
        features = []
        results = await request.app.t38.scan(key).asObjects()
        for obj in results.objects:
            geo = obj.object
            p = Properties(key=key, id=obj.id)
            f = Feature(type="Feature", properties=p, geometry=geo)
            features.append(f)
        return features
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)


@router.get("/{key}/{id}")
async def get_feature_by_id(key: str, id: str, request: Request):
    try:
        result = await request.app.t38.get(key, id).asObject()
        p = Properties(key=key, id=id)
        f = Feature(type="Feature", properties=p, geometry=result.object)
        return f
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)
