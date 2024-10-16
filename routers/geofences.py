from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.geofence import Geofence

router = APIRouter(prefix="/geofences", tags=["geofences"])


@router.post("/")
async def create_geofence(request: Request, geofence: Geofence = Body(...)):
    t38 = request.app.t38
    area_id = geofence.area_key
    object_key = geofence.object_key
    try:
        obj = await t38.get("zones", area_id).asObject()
        hook = t38.sethook(geofence.name, geofence.url)
        if obj.object['type'] == "Polygon":
            await hook.within(object_key).detect(geofence.events).get("zones", area_id).activate()
        else:
            await hook.nearby(object_key).detect(geofence.events).point(
                *obj.object['coordinates'], geofence.radius).activate()
        return JSONResponse(content={"message": "Geofence created"}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)


@router.get("/")
async def read_geofences(request: Request):
    try:
        geofences = []
        results = await request.app.t38.command("HOOKS", "*")
        for r in results['hooks']:
            url = r['endpoints'][0]
            key = r['command'][6]
            zone = r['command'][7]
            events = list(r['command'][4].split(','))

            g = Geofence(name=r['name'], url=url,
                         events=events, key=key,
                         zone=zone)
            geofences.append(g)
        return JSONResponse(content=jsonable_encoder(geofences), status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)


@router.get("/{name}")
async def read_geofence(name: str, request: Request):
    try:
        result = await request.app.t38.command("HOOKS", [name])
        if result['hooks']:
            r = result['hooks'][0]
            url = r['endpoints'][0]
            key = r['command'][6]
            zone = r['command'][7]
            events = list(r['command'][4].split(','))

            g = Geofence(name=r['name'], url=url,
                         events=events, key=key,
                         zone=zone)
            return JSONResponse(content=jsonable_encoder(g), status_code=200)
        return JSONResponse(content=jsonable_encoder({}), status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)


@router.delete("/{name}")
async def delete_geofence(name: str, request: Request):
    try:
        result = await request.app.t38.command("DELHOOK", [name])
        if result['ok']:
            return JSONResponse(content={"message": "Geofence deleted"}, status_code=200)
        else:
            return JSONResponse(content={"message": "Error"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)
