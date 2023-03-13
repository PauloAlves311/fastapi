from fastapi import FastAPI
import json
from urllib.parse import urlparse
# from typing import Union
# from fastapi.responses import PlainTextResponse
# from pydantic import BaseModel

app = FastAPI()

load = json.load(open("data.json"))["imoveis"]["imovel"]

@app.get("/")
async def read_index():
    houses = []
    destaque = 0
    for house in load:
        for imagem in house["multimedia"]["imagem"]:
            if type(imagem) is str:
                url = "https://cdn1.ximocrm.com/i/704ED61D-335D-46AF-813E-00DD2E2BB6F4_" + house["id"] + "_0______" + urlparse(house["multimedia"]["imagem"]["url"]).path.rsplit('/', 1)[-1]
            elif type(imagem) is dict:
                if imagem["principal"] == "1":
                    url = "https://cdn1.ximocrm.com/i/704ED61D-335D-46AF-813E-00DD2E2BB6F4_" + house["id"] + "_0______" + urlparse(imagem["url"]).path.rsplit('/', 1)[-1]

        houses.append({
            "id": house["id"],
            "sort": house["ref"],
            "titulo": house["titulo"],
            "preco": house["precoweb"],
            "url": url,
             })

        if house["destaque"] == "1":
            destaque += 1
    print(destaque)

    return houses
            


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
                "freguesia": house["freguesia"]["#text"] if house["freguesia"]["@id"] != "0" else "",
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








@app.get("/houseOriginal/{house_id}")
async def find_house(house_id: str):
    for house in load:
        if house_id == house["id"]:
            return house



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