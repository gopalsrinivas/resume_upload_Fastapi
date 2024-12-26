from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.careersServices import (
    create_careeruser,
    get_all_users,
    get_user_by_id,
)
from app.schemas.careersSchemas import (
    CareerUserCreate,
    CareerUserResponse,
    PaginatedCareerUsersResponse,
)
from app.core.logging import logging

router = APIRouter()


@router.post("/", summary="Create new User Registration")
async def register_careeruser(
    name: str = Form(..., description="User's full name"),
    email: str = Form(..., description="User's email address"),
    mobile: str = Form(..., description="User's mobile number"),
    resume_file: UploadFile = File(..., description="Resume file upload"),
    db: AsyncSession = Depends(get_db),
):
    logging.info(f"Received request to register user: {name}, {email}, {mobile}")
    try:
        # Attempt to create a new user
        new_user = await create_careeruser(
            db, name=name, email=email, mobile=mobile, resume_file=resume_file
        )
        logging.info(f"User registered successfully: {new_user.user_id}")

        # Return the desired structured response
        return {
            "status_code": 200,
            "message": "User registered successfully.",
            "user_data": {
                "id": new_user.id,
                "user_id": new_user.user_id,
                "name": new_user.name,
                "email": new_user.email,
                "mobile": new_user.mobile,
                "resume_filename": new_user.resume_filename,
                "is_active": new_user.is_active,
                "created_on": new_user.created_on,
                "updated_on": new_user.updated_on,
            },
        }
    except HTTPException as http_exc:
        logging.error(f"HTTPException during user registration: {http_exc.detail}")
        raise http_exc
    except ValueError as val_err:
        logging.warning(f"ValueError during user registration: {str(val_err)}")
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as exc:
        logging.error(f"Unexpected error during user registration: {str(exc)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during user registration. Please try again later.",
        )


@router.get(
    "/",
    response_model=PaginatedCareerUsersResponse,
    summary="Get all active User Detail",
)
async def get_all_active_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db),
):
    logging.info(f"Request to fetch all active users with skip={skip}, limit={limit}")
    try:
        users, total_count = await get_all_users(db, skip, limit)
        return {
            "status_code": 200,
            "message": "Users retrieved successfully",
            "total_users": total_count,
            "users": [CareerUserResponse.from_orm(user) for user in users],
        }
    except HTTPException as ex:
        logging.error(f"Failed to fetch users: {str(ex.detail)}", exc_info=True)
        raise ex
    except Exception as e:
        logging.error(f"Unexpected error fetching users: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{id}", response_model=dict, summary="Get user by ID")
async def get_user_by_id_route(id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Log the request to fetch user by ID
        logging.info(f"Request to fetch user with ID: {id}")

        # Fetch the user from the database
        user = await get_user_by_id(db, id)

        # If user not found, return 404 response
        if not user:
            logging.warning(f"User with ID {id} not found")
            return {"msg": "User not found", "status_code": 404, "data": None}

        # Check if the user is inactive
        if not user.is_active:
            logging.warning(f"User with ID {id} is inactive.")
            return {"msg": "User inactive", "status_code": 403, "data": None}

        # If the user is active, return the user data
        logging.info(f"User retrieved successfully: {user.id}")
        return {
            "msg": "User retrieved successfully",
            "status_code": 200,
            "data": CareerUserResponse.from_orm(user),
        }

    except HTTPException as he:
        logging.error(f"HTTP error: {he.detail}", exc_info=True)
        raise he

    except Exception as e:
        logging.error(f"Failed to fetch user: {str(e)}", exc_info=True)
        return {"msg": "Internal server error", "status_code": 500, "data": None}
