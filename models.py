from datetime import date
from enum import Enum
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship


class GenreUrl(str, Enum):
    ROCK = "rock"
    METAL = "metal"
    GRUNGE = "grunge"
    ELECTRONIC = "electronic"
    SHOEGAZE = "shoegaze"


class GenreChoices(str, Enum):
    ROCK = "Rock"
    METAL = "Metal"
    GRUNGE = "Grunge"
    ELECTRONIC = "Electronic"
    SHOEGAZE = "Shoegaze"


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int | None = Field(default=None, foreign_key="band.id")


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None

    @field_validator("genre", mode="before")
    def title_case(cls, v):
        return v.title()  # rock -> Rock


class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")

# _-------------------------------------------------------------------------_#
# Below is the code without SQLModel
# _-------------------------------------------------------------------------_#
# from datetime import date
# from enum import Enum
# from pydantic import BaseModel, field_validator
# from sqlmodel import SQLModel, Field

# class GenreUrl(str, Enum):
#     ROCK = "rock"
#     METAL = "metal"
#     GRUNGE = "grunge"
#     ELECTRONIC = "electronic"
#     SHOEGAZE = "shoegaze"


# class GenreChoices(str, Enum):
#     ROCK = "Rock"
#     METAL = "Metal"
#     GRUNGE = "Grunge"
#     ELECTRONIC = "Electronic"
#     SHOEGAZE = "Shoegaze"


# class Album(BaseModel):
#     title: str
#     release_date: date


# class BandBase(BaseModel):
#     name: str
#     genre: GenreChoices
#     albums: list[Album] = []


# class BandCreate(BandBase):
#     @field_validator("genre", mode="before")
#     def title_case(cls, v):
#         return v.title()  # rock -> Rock


# class BandWithID(BandBase):
#     id: int
