from fastapi import FastAPI, HTTPException
import json
from urllib.parse import urlparse
from typing import Optional, Union
from pydantic import BaseModel
# from typing import Union
# from fastapi.responses import PlainTextResponse


import download
download.downloadData()

app = FastAPI()

load = json.load(open("data.json"))["imoveis"]["imovel"]


@app.get("/")
async def read_index(
    page: Optional[int] = 1,
    limit: Optional [int] = 20,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    obj: Optional[str] = None,
    zona: Optional[str] = None,
    apiKey: Optional[str] = None,
    ):
    houses = []
    destaque = 0

    if apiKey != "aBAajadf28318aAJSlas892394NQalsASJD893124lasdSADLshdoashsfo":
        raise HTTPException(status_code=401, detail="Invalid API key")

    for house in load:
        for imagem in house["multimedia"]["imagem"]:
            if type(imagem) is str:
                url = "https://cdn1.ximocrm.com/i/704ED61D-335D-46AF-813E-00DD2E2BB6F4_" + house["id"] + "_0______" + urlparse(house["multimedia"]["imagem"]["url"]).path.rsplit('/', 1)[-1]
            elif type(imagem) is dict:
                if imagem["principal"] == "1":
                    url = "https://cdn1.ximocrm.com/i/704ED61D-335D-46AF-813E-00DD2E2BB6F4_" + house["id"] + "_0______" + urlparse(imagem["url"]).path.rsplit('/', 1)[-1]
        
        if "Land" in house["tipo"]["#text"] or "Plot" in house["tipo"]["#text"]:
            titulo = house["tipo"]["#text"]
        else:
            titulo = house["tipo"]["#text"] + ", T" + house["nquartos"]

        if zona and house["localidade"] != zona:
            continue

        if obj and house["objectivo"]["#text"] != obj:
            continue

        if (min_price and int(house["precoweb"]) < min_price) or (max_price and int(house["precoweb"]) > max_price):
            continue

        houses.append({
            "id": house["id"],
            "sort": house["ref"],
            "titulo": titulo,
            "zona": house["localidade"],
            "preco": house["precoweb"],
            "objectivo": house["objectivo"]["#text"],
            "nQuartos": house["nquartos"],
            "imagem": url,
             })

        if house["destaque"] == "1":
            destaque += 1


    # Calculate the start and end indexes of the slice
    start = (page - 1) * limit
    end = start + limit

    # Slice the houses list to return only the requested items
    paginated_houses = houses[start:end]

    # Calculate the total number of pages
    total_pages = (len(houses) + limit - 1) // limit

    # return houses
    return {
        # "start_index": start,
        # "end_index": end,
        "total_pages": total_pages,
        "count": len(houses),
        "destaque_count": destaque,
        "houses": paginated_houses,
    }



@app.get("/house/{house_id}")
async def find_house(house_id: str):
    for house in load:
        if house_id == house["id"]:
            imovel = {
                "id": house["id"],
                "sort": house["ref"],
                "tipo": house["tipo"]["#text"],
                "tipologia": house["tipologia"]["#text"] if house["tipologia"]["@id"] != "0" else "N/A",
                "estado": house["estado"]["#text"] if house["estado"]["@id"] != "0" else "N/A",
                "objectivo": house["objectivo"]["#text"] if house["objectivo"]["@id"] != "0" else "N/A",
                "distrito": house["distrito"]["#text"] if house["distrito"]["@id"] != "0" else "N/A",
                "concelho": house["concelho"]["#text"] if house["concelho"]["@id"] != "0" else "N/A",
                "freguesia": house["freguesia"]["#text"] if house["freguesia"]["@id"] != "0" else "N/A",
                "zona": house["zona"],
                "localidade": house["localidade"],
                "cp": house["cp"],
                "regiao": house["segmento"],
                "coordenadas": house["mapa_coord"],
                "areautil": house["areautil"],
                "areabruta": house["areabruta"],
                "areabrutaprivada": house["areabrutaprivada"],
                "areaterreno": house["areaterreno"],
                "anoconstrucao": house["construcaoano"],
                "nquartos": house["nquartos"],
                "preco": house["precoweb"],
            }
    return imovel

            



@app.get("/media/{house_id}")
async def find_media(house_id: str):
    media = []
    for house in load:
        if house_id == house["id"]:
            media.append(
                house["multimedia"]["imagem"] #Add new urls here
                )
        return media




@app.get("/localidades")
async def get_localidades():
    localidades = set()
    for house in load:
        localidades.add(house["localidade"])
    localidades_list = list(localidades)
    localidades_list.sort()
    return {"location": localidades_list}








# @app.get("/houseOriginal/{house_id}")
# async def find_house(house_id: str):
#     for house in load:
#         if house_id == house["id"]:
#             return house



# @app.get("/mediadebug/{house_id}")
# async def find_media(house_id: str):
#     for house in load:
#         if house_id == house["id"]:
#             for imagem in house["multimedia"]["imagem"]:
#                 if imagem["principal"] == "1":
#                     return imagem["url"]





# @app.get("/abc")
# async def read_root():
#     houses = []
#     for house in load:
#         houses.append({
#                 "id": house["id"],
#                   })
#         houses.append({
#                 "titulo": house["titulo"],
#                   })
#         for imagem in house["multimedia"]["imagem"]:
#             # houses.append({imagem["url"]})
#             if imagem["principal"] == "1":
#                 houses.append({"imagem": imagem["url"]})
#             # else:
#                 # houses.append({"image": imagem["url"]})
            
#         return houses        