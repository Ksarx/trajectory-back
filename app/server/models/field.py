from typing import Optional, List

from pydantic import BaseModel, Field

class FieldModelItem(BaseModel):
    name: str = Field(...)
    disciplines: List[str] = Field(...)
    
class FieldModelSchema(BaseModel):
    direction: str = Field(...)
    profile: str = Field(...)
    fields: List[FieldModelItem] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "direction": "Фундаментальная информатика и информационные технологии",
                "profile": "Информатика и компьютерные науки",
                "fields": [{"name": 'математический задача решение основной', 
                            'disciplines': ['Численные методы',
                            'Математический анализ',
                            'Математические методы прогнозирования',
                            'Математическая логика и теория алгоритмов',
                            'Дифференциальные уравнения'],},
                    ],
            }
        }


class UpdateFieldModel(BaseModel):
    fields: List[FieldModelItem] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fields": [{"name": 'математический задача решение основной', 
                            'disciplines': ['Численные методы',
                            'Математический анализ',
                            'Математические методы прогнозирования',
                            'Математическая логика и теория алгоритмов',
                            'Дифференциальные уравнения'],},
                    ],
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}