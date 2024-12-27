from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, HttpUrl

PyObjectId = Annotated[str, BeforeValidator(str)]


class LongURL(BaseModel):
    url: HttpUrl


class ShortURL(BaseModel):
    id: PyObjectId = Field(alias="_id")
    url: HttpUrl
    shortCode: str
    createdAt: datetime
    updatedAt: datetime
    model_config = ConfigDict(from_attributes=True)


class ShortURLStats(ShortURL):
    accessCount: int
    model_config = ConfigDict(from_attributes=True)


class NotFoundException(BaseModel):
    detail: str = "Not Found"
