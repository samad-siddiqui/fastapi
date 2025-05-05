from fastapi import FastAPI, HTTPException, Depends
from models import GenreUrl, Band, BandCreate, Album
from sqlmodel import Session
from contextlib import asynccontextmanager
from db import init_db, get_session
from sqlmodel import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/bands")
async def create_band(
    band: BandCreate,
    session: Session = Depends(get_session)
     ):
    band = Band(name=band.name, genre=band.genre)
    session.add(band)
    if band.albums:
        for album in band.albums:
            album_obj = Album(
                title=album.title,
                release_date=album.release_date,
                band=band
            )
            session.add(album_obj)
            # session.commit()
    session.add(band)
    session.commit()
    session.refresh(band)
    return band


@app.get("/bands/{band_id}")
async def get_band(band_id: int, session: Session = Depends(get_session)):

    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return band


@app.get("/bands")
async def get_bands(genre: GenreUrl | None = None,
                    has_albums: bool = False,
                    session: Session = Depends(get_session)):
    band_list = session.exec(select(Band)).all()

    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
            ]
    if has_albums:
        band_list = [b for b in band_list if len(b.albums) > 0]
        # print(bands)
    return band_list

# _-------------------------------------------------------------------------_#
# Below is the code without SQLModel
# from fastapi import FastAPI, HTTPException
# from models import GenreUrl, BandWithID, BandCreate

# app = FastAPI()


# BANDS = [
#     {"id": 1, "name": "The Beatles", "genre": "Rock"},
#     {"id": 2, "name": "The Rolling Stones", "genre": "Rock"},
#     {"id": 3, "name": "Nirvana", "genre": "Grunge", "albums": [
#         {"title": "Nevermind", "release_date": "1991-09-24"},
#         {"title": "In Utero", "release_date": "1993-09-21"},
#     ]},
#     {"id": 4, "name": "Metallica", "genre": "Metal"},
#     {"id": 5, "name": "Queen", "genre": "Rock"},
#     {"id": 6, "name": "Pink Floyd", "genre": "Rock"},
#     {"id": 7, "name": "Led Zeppelin", "genre": "Rock"},
#     {"id": 8, "name": "The Who", "genre": "Rock"},
#     {"id": 9, "name": "AC/DC", "genre": "Shoegaze"},
#     {"id": 10, "name": "Guns N' Roses", "genre": "Electronic"},
# ]


# @app.get("/bands")
# async def get_bands(genre: GenreUrl | None = None,
#                     has_albums: bool = False):

#     band_list = [BandWithID(**b) for b in BANDS]

#     if genre:
#         band_list = [
#             b for b in band_list if b.genre.value.lower() == genre.value
#             ]
#     if has_albums:
#         band_list = [b for b in band_list if len(b.albums) > 0]
#         # print(bands)
#     return band_list


# @app.get("/bands/{band_id}")
# async def get_band(band_id: int):
#     for band in BANDS:
#         if band["id"] == band_id:
#             return BandWithID(**band)
#     raise HTTPException(status_code=404, detail="Band not found")


# @app.get("/bands/genre/{genre}")
# async def get_band_by_genre(genre: GenreUrl):
#     bands_by_genre = [b for b in BANDS if b["genre"].lower() ==
#                       genre.value]
#     if not bands_by_genre:
#         raise HTTPException(status_code=404,
#                             detail="No bands found for this genre")
#     return bands_by_genre


# @app.post("/bands")
# async def create_band(band: BandCreate):
#     id = BANDS[-1]["id"] + 1
#     band = BandWithID(id=id, **band.model_dump()).model_dump()
#     BANDS.append(band)
#     return band
