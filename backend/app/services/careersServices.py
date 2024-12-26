from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func, and_
from app.models.careersModel import CareersUsers
from app.services.s3_upload import upload_file_to_s3
from app.core.logging import logging


async def generate_user_id(db: AsyncSession) -> str:
    """Generate a unique user ID."""
    try:
        result = await db.execute(
            select(CareersUsers).order_by(CareersUsers.id.desc()).limit(1)
        )
        latest_user = result.scalar_one_or_none()
        if latest_user:
            last_id = int(latest_user.user_id.split("_")[-1])
            return f"user_{last_id + 1}"
        return "user_1"
    except Exception as e:
        logging.error(f"Error generating user ID: {e}")
        raise HTTPException(status_code=500, detail="Error generating user ID")


async def create_careeruser(
    db: AsyncSession, name: str, email: str, mobile: str, resume_file: UploadFile
) -> CareersUsers:
    """Create a new career user record."""
    try:
        logging.info("Checking if the email and mobile already exist in the database.")
        existing_user = await db.execute(
            select(CareersUsers).filter(
                and_(CareersUsers.email == email, CareersUsers.mobile == mobile)
            )
        )
        user = existing_user.scalar_one_or_none()

        if user:
            logging.warning("Both email and mobile number already exist.")
            raise HTTPException(
                status_code=400, detail="Both email and mobile number already exist"
            )

        logging.info("Generating a new user ID.")
        user_id = await generate_user_id(db)

        logging.info("Uploading resume to S3.")
        resume_filename = f"{user_id}_{resume_file.filename}"
        resume_url = await upload_file_to_s3(resume_file, resume_filename)

        logging.info("Creating a new user record in the database.")
        new_user = CareersUsers(
            user_id=user_id,
            name=name,
            email=email,
            mobile=mobile,
            resume_filename=resume_url,
            is_active=True,
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logging.info("User created successfully.")
        return new_user

    except HTTPException as http_exc:
        logging.error(f"HTTP Exception: {http_exc.detail}")
        raise http_exc

    except Exception as e:
        logging.exception("Unexpected error during user creation.")
        raise HTTPException(status_code=500, detail="Error during user creation")


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    try:
        logging.info(f"Fetching users with skip={skip}, limit={limit}")

        # Fetch active users with pagination
        result = await db.execute(
            select(CareersUsers)
            .where(CareersUsers.is_active == True)
            .order_by(CareersUsers.id.desc())
            .offset(skip)
            .limit(limit)
        )
        users = result.scalars().all()

        # Get the total count of active users
        total_count_result = await db.execute(
            select(func.count(CareersUsers.id)).where(CareersUsers.is_active == True)
        )
        total_count = total_count_result.scalar()

        logging.info(
            f"Successfully retrieved {len(users)} users. Total count: {total_count}"
        )
        return users, total_count

    except Exception as e:
        logging.error(f"Failed to fetch users: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch users.")


async def get_user_by_id(db: AsyncSession, id: int):
    try:
        logging.info(f"Fetching user with ID: {id}")

        # Fetch user by ID
        user = await db.get(CareersUsers, id)
        if not user:
            logging.warning(f"User with ID {id} not found")
            return None

        logging.info(f"Successfully retrieved user: {user.id}")
        return user

    except Exception as e:
        logging.error(f"Error retrieving user by ID {id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")
