from datetime import date, datetime, timezone
from enum import Enum
from pydantic import (
    field_validator,
    EmailStr,
    model_validator,
    BaseModel
)
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


class TaskBase(SQLModel):
    title: str
    task: str
    description: str | None = None
    due_date: date | None = None


class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    completed: bool = Field(default=False)

    @field_validator("task", mode="before")
    def title_case(cls, v):
        return v.title()


class ProfileBase(SQLModel):
    name: str
    email: EmailStr
    password: str
    disabled: bool = False


class Profile(ProfileBase, table=True):
    id: int = Field(default=None, primary_key=True)
    feedbacks: list["Feedback"] = Relationship(back_populates="profile")
    # tasks: list[Task] = Relationship(back_populates="profile")
    # bands: list[Band] = Relationship(back_populates="profile")


class ProfileRegister(ProfileBase):
    confirm_password: str

    @model_validator(mode="before")
    def password_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        return values

    @field_validator("email", mode="before")
    def email_lower(cls, v):
        return v.lower()  # rock -> Rock


class FeedbackBase(SQLModel):

    email: EmailStr
    message: str
    user_id: int = Field(default=None, foreign_key="profile.id")
    file_path: str | None = None
# default_factory calls the function at run time while default will uses a
# fixed value
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        )


class Feedback(FeedbackBase, table=True):
    id: int = Field(default=None, primary_key=True)
    profile: Profile = Relationship(back_populates="feedbacks")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # username: str | None = None
    email: EmailStr | None = None
