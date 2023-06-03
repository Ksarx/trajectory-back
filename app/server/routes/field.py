from fastapi import APIRouter, Body, UploadFile, File
from fastapi.encoders import jsonable_encoder
import os

from server.clustering import (
    model_work,
)
from server.database import (
    retrieve_fields,
    retrieve_field,
    add_field,
    update_field,
    delete_field,
)
from server.models.field import (
    FieldModelSchema,
    UpdateFieldModel,
    ErrorResponseModel,
    ResponseModel,
)

router = APIRouter()

@router.get("", response_description="Fields retrieved")
async def get_fields():
    fields = await retrieve_fields()
    if fields:
        return ResponseModel(fields, "Fields data retrieved successfully")
    return ResponseModel(fields, "Empty list returned")

@router.get("/{directionId}", response_description="Field data retrieved")
async def get_field_data(directionId: int):
    field = await retrieve_field(directionId)
    if field:
        return ResponseModel(field, "Field data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Field doesn't exist.")

@router.post("/upload/{direction}/{profile}", response_description="Field successfully added into the database")
async def upload_file(direction: str, profile: str, file: UploadFile = File(...)):
    try:
        temp_file_path = f"{file.filename}"
        contents = file.file.read()
        with open(temp_file_path, 'wb') as f:
            f.write(contents)
        
        result: FieldModelSchema = model_work(temp_file_path, direction, profile)
        os.remove(temp_file_path)
        new_field = await add_field(result, direction, profile)
        if new_field:
            return ResponseModel(new_field, 'Field added succesfully')
        return ErrorResponseModel("An error occurred.", 404, "No data with that direction name and profile name found")
        

    except Exception:
        return ErrorResponseModel("An error occurred.", 400, "Error with file uploading")
    finally:
        file.file.close()
    
@router.put("/{directionId}")
async def update_field_data(directionId: int, req: UpdateFieldModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_job = await update_field(directionId, req)
    if updated_job:
        return ResponseModel(
            "Field with directionId: {} update is successful".format(directionId),
            "Field updated successfully",
         )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the field data.",
    )
        
@router.delete("/{directionId}", response_description="Field data deleted from the database")
async def delete_field_data(directionId: int):
    deleted_field = await delete_field(directionId)
    if deleted_field:
        return ResponseModel(
            "Field with directionId: {} removed".format(directionId), "Field deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Field with directionId: {} doesn't exist".format(directionId)
    )