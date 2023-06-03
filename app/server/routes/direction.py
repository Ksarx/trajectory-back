from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    retrieve_directions,
    retrieve_direction,
    retrieve_direction_names,
    retrieve_directions_faculties,
    add_direction,
    update_direction,
    delete_direction,
)

from server.models.direction import (
    DirectionSchema,
    UpdateDirectionModel,
    ResponseModel,
    ErrorResponseModel
)

router = APIRouter()


@router.get("", response_description="Directions retrieved")
async def get_directions():
    directions = await retrieve_directions()
    if directions:
        return ResponseModel(directions, "Directions data retrieved successfully")
    return ResponseModel(directions, "Empty list returned")

@router.get("/{id}", response_description="Direction data retrieved")
async def get_direction_data(id: int):
    direction = await retrieve_direction(id)
    if direction:
        return ResponseModel(direction, "Direction data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Job doesn't exist.")

@router.get("/search/{jobId}", response_description="Directions names for search retrieved")
async def get_direction_names(jobId: int, search_query: str | None = None):
    filters = {}
    filters['idJobs'] = {"$in": [jobId]}
    if search_query:
        filters["name"] = {"$regex": search_query, "$options": "i"}
    directions = await retrieve_direction_names(filters)
    if directions:
        return ResponseModel(directions, "Directions names retrieved successfully")
    return ResponseModel(directions, "Empty list returned")

@router.get("/faculties/", response_description="Direction faculties retrieved")
async def get_direction_names():
    faculties = await retrieve_directions_faculties()
    if faculties:
        return ResponseModel(faculties, "Directions faculties retrieved successfully")
    return ResponseModel(faculties, "Empty list returned")


@router.post("", response_description="Direction added into the database")
async def add_direction_data(direction: DirectionSchema = Body(...)):
    direction = jsonable_encoder(direction)
    new_direction = await add_direction(direction)
    return ResponseModel(new_direction, "Direction added successfully.")

@router.put("/{id}")
async def update_direction_data(id: int, req: UpdateDirectionModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_direction = await update_direction(id, req)
    if updated_direction:
        return ResponseModel(
            "Direction with ID: {} name update is successful".format(id),
            "Direction updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the direction data.",
    )


@router.delete("/{id}", response_description="Direction data deleted from the database")
async def delete_direction_data(id: int):
    deleted_direction = await delete_direction(id)
    if deleted_direction:
        return ResponseModel(
            "Direction with ID: {} removed".format(id), "Direction deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Direction with id {0} doesn't exist".format(id)
    )