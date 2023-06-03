# from typing import Optional, List

# from pydantic import BaseModel, EmailStr, Field

# class TrajectorySchema(BaseModel):
#     directionId: int = Field(...)
#     jobId: int = Field(...)
#     trajectory: List[str] = Field(...)

#     class Config:
#         schema_extra = {
#             "example": {
#                 "directionId": "09.03.01",
#                 "jobId": "Информатика и вычислительная техника",
#                 "trajectory": [
#                                 'Дискретная математика',
#                                 'Математическая логика и теория алгоритмов',
#                                 'Оптимизация и принятие решений',
#                                 'Машинное обучение',
#                                 'Математические основы защиты информации',
#                                 'Большие данные',
#                                 'Bi решения и многомерный анализ данных',
#                                 'СУБД',
#                                 'Базы данных',
#                                 'Web-разработка',
#                                 'Проектная деятельность',
#                                 'Алгоритмизация и программирование',
#                                 'Практикум по программированию',
#                                 'Объектно-оринтированный анализ и проектирование',
#                                 'Администрирование БД',
#                                 'SQL и получение данных',
#                                 'Программная инженерия',
#                                 'Геометрия',
#                                 'Алгебра',
#                                 'Теория чисел',
#                                 'Математический анализ',
#                                 'Правовое обеспечение профессиональной деятельности',
#                                 'Технологическое предпринимательство',
#                             ],
#             }
#         }


# class UpdateTrajectoryModel(BaseModel):
#     code: str = Field(...)
#     name: str = Field(...)
#     level: str = Field(...)
#     faculty: str = Field(...)
#     profile: str = Field(...)
#     description: str = Field(...)
#     idJobs: List[int] = Field(...)

#     class Config:
#         schema_extra = {
#             "example": {
#                 "code": "09.03.01",
#                 "name": "Информатика и вычислительная техника",
#                 "level": "Бакалавр 4 года, очно",
#                 "faculty": "ФИТиКС",
#                 "profile": "Технологии искуственного интеллекта",
#                 "description": "Бла бла бла бла бла бла бла бла",
#                 "idJobs": [1, 2, 3, 4],
#             }
#         }


# def ResponseModel(data, message):
#     return {
#         "data": data,
#         "code": 200,
#         "message": message,
#     }
    
# def ErrorResponseModel(error, code, message):
#     return {"error": error, "code": code, "message": message}