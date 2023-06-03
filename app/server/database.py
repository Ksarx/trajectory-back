import motor.motor_asyncio
from bson.objectid import ObjectId
import math

# MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://Artemy:Pass321@cluster0.rnjzlbf.mongodb.net/atlas?retryWrites=true&w=majority')

database = client.atlas
job_collection = database.get_collection("jobs")
field_collection = database.get_collection("fields")
direction_collection = database.get_collection("directions")


# Helpers

def job_helper(job) -> dict:
    return {
        "id": job["id"],
        "name": job["name"],
        "description": job["description"],
        "skills": job["skills"],
        "field": job["field"],
    }
    
def direction_helper(direction) -> dict:
    return {
        "id": direction["id"],
        "code": direction["code"],
        "name": direction["name"],
        "level": direction["level"],
        "faculty": direction["faculty"],
        "profile": direction["profile"],
        "description": direction["description"],
        "idJobs": direction["idJobs"],
    }
    
def field_helper(field) -> dict:
    return {
        "direction": field['direction'],
        "profile": field['profile'],
        "fields": field['fields'],
    }


# crud operations

#### Field ####

# GET all fields
async def retrieve_fields():
    fields = []
    async for field in field_collection.find():
        fields.append(field_helper(field))
    return fields

# GET specific field
async def retrieve_field(id: int) -> dict:
    field = await field_collection.find_one({"directionId": id})
    if field:
        return field_helper(field)

async def add_field(data: dict, direction_name: str, profile_name: str) -> dict:
    direction = await direction_collection.find_one({"name": direction_name, "profile": profile_name})
    if direction:
        data["directionId"] = direction["id"]
        field = await field_collection.insert_one(data)
        new_field = await field_collection.find_one({"_id": field.inserted_id})
        return field_helper(new_field)

# UPDATE specific field
async def update_field(id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    field = await field_collection.find_one({"directionId": id})
    if field:
        updated_field = await field_collection.update_one(
            {"directionId": id}, {"$set": data}
        )
        if updated_field:
            return True
        return False

# DELETE specific field
async def delete_field(id: int):
    field = await field_collection.find_one({"directionId": id})
    if field:
        await field_collection.delete_one({"directionId": id})
        return True
    
#### Job ####

# GET all jobs
async def retrieve_jobs(skip: int, limit: int, filters: dict):
    total_count = await job_collection.count_documents(filters)
    total_pages = math.ceil(total_count / limit)
    jobs = []
    async for job in job_collection.find(filters).skip(skip).limit(limit):
        jobs.append(job_helper(job))
    return jobs, total_pages, total_count

# GET specific job
async def retrieve_job(id: int) -> dict:
    job = await job_collection.find_one({"id": id})
    if job:
        return job_helper(job)
    
# GET job names
async def retrieve_jobs_names(search: str = None) -> dict:
    if search:
        jobs = await job_collection.distinct("name", {"name": {"$regex": search, "$options": "i"}})
    else:
        jobs = []
    return jobs

# GET job skills
async def retrieve_jobs_skills() -> dict:
    skills = await job_collection.distinct("skills")
    return skills

# GET job fields
async def retrieve_jobs_fields() -> dict:
    fields = await job_collection.distinct("field")
    return fields

# POST job
async def add_job(data: dict) -> dict:
    num = await job_collection.count_documents({})
    data["id"] = num + 1
    job = await job_collection.insert_one(data)
    new_job = await job_collection.find_one({"_id": job.inserted_id})
    return job_helper(new_job)

# UPDATE specific job 
async def update_job(id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    job = await job_collection.find_one({"id": id})
    if job:
        updated_job = await job_collection.update_one(
            {"id": id}, {"$set": data}
        )
        if updated_job:
            return True
        return False

# DELETE specific job
async def delete_job(id: int):
    job = await job_collection.find_one({"id": id})
    if job:
        await job_collection.delete_one({"id": id})
        return True
    
#### Direction ####

# GET all directions
async def retrieve_directions():
    directions = []
    async for direction in direction_collection.find():
        directions.append(direction_helper(direction))
    return directions

# GET specific direction
async def retrieve_direction(id: int) -> dict:
    direction = await direction_collection.find_one({"id": id})
    if direction:
        return direction_helper(direction)
    
# GET specific job directions
async def retrieve_job_directions(skip: int, limit: int, filters: dict) -> dict:
    total_count = await direction_collection.count_documents(filters)
    total_pages = math.ceil(total_count / limit)
    
    directions = []
    async for direction in direction_collection.find(filters).skip(skip).limit(limit):
        directions.append(direction_helper(direction))
    return directions, total_pages, total_count

# GET directions names
async def retrieve_direction_names(filters: dict) -> dict:
    if "name" in filters:
        directions = await direction_collection.distinct("name", filters)
    else:
        directions = []
    return directions

# GET direction faculties
async def retrieve_directions_faculties() -> dict:
    faculties = await direction_collection.distinct("faculty")
    return faculties
 
# POST direction
async def add_direction(data: dict) -> dict:
    num = await direction_collection.count_documents({})
    data["id"] = num + 1
    idJobs = []
    for job_name in data["jobs"]:
        search = await job_collection.find_one({"name": job_name})
        if search:
            idJobs.append(search["id"])
    data.pop('jobs')
    data['idJobs'] = idJobs
    direction = await direction_collection.insert_one(data)
    new_direction = await direction_collection.find_one({"_id": direction.inserted_id})
    return direction_helper(new_direction)

# UPDATE specific direction 
async def update_direction(id: int, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    direction = await direction_collection.find_one({"id": id})
    if direction:
        updated_direction = await direction_collection.update_one(
            {"id": id}, {"$set": data}
        )
        if updated_direction:
            return True
        return False

# DELETE specific direction
async def delete_direction(id: int):
    direction = await direction_collection.find_one({"id": id})
    if direction:
        await direction_collection.delete_one({"id": id})
        return True
