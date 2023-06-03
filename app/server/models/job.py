from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field


class JobSchema(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    skills: List[str] = Field(...)
    field: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Frontend-разработчик",
                "description": "Благодаря frontend-разработчикам мы оставляем лайки и комментарии",
                "skills": ["Верстка", "Создание сайтов"],
                "field": "Дизайн",
            }
        }


class UpdateJobModel(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    skills: List[str] = Field(...)
    field: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Frontend-разработчик",
                "description": "Благодаря frontend-разработчикам мы оставляем лайки и комментарии",
                "skills": ["Верстка", "Создание сайтов"],
                "field": "Дизайн",
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