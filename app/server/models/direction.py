from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field

class DirectionSchema(BaseModel):
    code: str = Field(...)
    name: str = Field(...)
    level: str = Field(...)
    faculty: str = Field(...)
    profile: str = Field(...)
    description: str = Field(...)
    jobs: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "code": "09.03.01",
                "name": "Информатика и вычислительная техника",
                "level": "Бакалавр 4 года, очно",
                "faculty": "ФИТиКС",
                "profile": "Технологии искуственного интеллекта",
                "description": "Бла бла бла бла бла бла бла бла",
                "jobs": ["Frontend-разработчик", "Переводчик"],
            }
        }


class UpdateDirectionModel(BaseModel):
    code: str = Field(...)
    name: str = Field(...)
    level: str = Field(...)
    faculty: str = Field(...)
    profile: str = Field(...)
    description: str = Field(...)
    idJobs: List[int] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "code": "09.03.01",
                "name": "Информатика и вычислительная техника",
                "level": "Бакалавр 4 года, очно",
                "faculty": "ФИТиКС",
                "profile": "Технологии искуственного интеллекта",
                "description": "Бла бла бла бла бла бла бла бла",
                "idJobs": [1, 2, 3, 4],
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }
    
def ResponseModelMeta(data, meta, message):
    return {
        "data": data,
        "meta": meta,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}