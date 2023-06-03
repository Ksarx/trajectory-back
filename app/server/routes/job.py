from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    retrieve_jobs,
    retrieve_job,
    retrieve_job_directions,
    retrieve_jobs_names,
    retrieve_jobs_skills,
    retrieve_jobs_fields,
    add_job,
    update_job,
    delete_job
)

from server.models.job import (
    JobSchema,
    UpdateJobModel,
    ResponseModel,
    ResponseModelMeta,
    ErrorResponseModel
)

router = APIRouter()


@router.get("", response_description="Jobs retrieved")
async def get_jobs(page: int = 1, limit: int = 6, field: str | None = None, skills: str | None = None, search: str | None = None):
    skip = (page - 1) * limit
    filters = {}
    if field:
        filters["field"] = {"$regex": field, "$options": "i"}
    if skills:
        skills_list = [skill.strip() for skill in skills.split(",")]
        filters["skills"] = {"$in": skills_list}
    if search:
        filters["name"] = {"$regex": search, "$options": "i"}
        
    jobs, total_pages, total_docs = await retrieve_jobs(skip, limit, filters)
    if jobs:
        meta = {
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "total_docs": total_docs,
        }
        return ResponseModelMeta(jobs, meta, "Jobs data retrieved successfully")
    return ResponseModel(jobs, "Empty list returned")

@router.get("/search", response_description="Jobs names for search retrieved")
async def get_jobs_names(search_query: str | None = None):
    jobs = await retrieve_jobs_names(search_query)
    if jobs:
        return ResponseModel(jobs, "Jobs names retrieved successfully")
    return ResponseModel(jobs, "Empty list returned")

@router.get("/{id}", response_description="Job data retrieved")
async def get_job_data(id: int):
    job = await retrieve_job(id)
    if job:
        return ResponseModel(job, "Job data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Job doesn't exist.")

@router.get("/{jobId}/directions", response_description="Job directions retrieved")
async def get_job_directions(jobId: int, page: int = 1, limit: int = 6, faculty: str | None = None, search: str | None = None):
    skip = (page - 1) * limit
    filters = {}
    filters["idJobs"] = {"$in": [jobId]}
    if faculty:
        faculty_list = [faculty.strip() for faculty in faculty.split(",")]
        filters["faculty"] = {"$in": faculty_list}
    if search:
        filters["name"] = {"$regex": search, "$options": "i"}
        
    directions, total_pages, total_docs = await retrieve_job_directions(skip, limit, filters)
    if directions:
        meta = {
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "total_docs": total_docs,
        }
        return ResponseModelMeta(directions, meta, "Job directions retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Job directions doesn't exist.")

@router.get("/skills/", response_description="Jobs skills retrieved")
async def get_jobs_skills():
    skills = await retrieve_jobs_skills()
    if skills:
        return ResponseModel(skills, "Jobs names retrieved successfully")
    return ResponseModel(skills, "Empty list returned")

@router.get("/fields/", response_description="Fields skills retrieved")
async def get_jobs_fields():
    fields = await retrieve_jobs_fields()
    if fields:
        return ResponseModel(fields, "Fields names retrieved successfully")
    return ResponseModel(fields, "Empty list returned")


@router.post("", response_description="Job added into the database")
async def add_job_data(job: JobSchema = Body(...)):
    job = jsonable_encoder(job)
    new_job = await add_job(job)
    return ResponseModel(new_job, "Job added successfully.")

@router.put("/{id}")
async def update_job_data(id: int, req: UpdateJobModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_job = await update_job(id, req)
    if updated_job:
        return ResponseModel(
            "Job with ID: {} name update is successful".format(id),
            "Job updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the job data.",
    )


@router.delete("/{id}", response_description="Job data deleted from the database")
async def delete_job_data(id: int):
    deleted_job = await delete_job(id)
    if deleted_job:
        return ResponseModel(
            "Job with ID: {} removed".format(id), "Job deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Job with id {0} doesn't exist".format(id)
    )