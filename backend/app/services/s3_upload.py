import boto3
from botocore.exceptions import NoCredentialsError, ClientError, BotoCoreError
from fastapi import HTTPException, UploadFile
from app.core.config import settings
from app.core.logging import logging

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)


async def upload_file_to_s3(file: UploadFile, file_name: str) -> str:
    logging.info(
        f"Attempting to upload file '{file.filename}' to S3 bucket '{settings.AWS_BUCKET}' with name '{file_name}'."
    )

    try:
        # Check if the file already exists in the S3 bucket
        try:
            s3_client.head_object(Bucket=settings.AWS_BUCKET, Key=file_name)
            logging.info(f"File '{file_name}' already exists. It will be replaced.")
        except ClientError as e:
            # If the file does not exist, it will throw a "Not Found" error (404)
            if e.response["Error"]["Code"] == "404":
                logging.info(f"File '{file_name}' does not exist. Uploading new file.")
            else:
                raise

        # Attempt to upload the file to S3 (this will overwrite the existing file)
        with file.file as f:
            s3_client.upload_fileobj(f, settings.AWS_BUCKET, file_name)

        file_url = f"https://{settings.AWS_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"
        logging.info(f"File uploaded successfully. File URL: {file_url}")
        return file_url

    except NoCredentialsError as no_cred_err:
        logging.error("AWS credentials are missing or invalid.")
        raise HTTPException(status_code=403, detail="AWS credentials not available.")

    except ClientError as client_err:
        error_message = client_err.response["Error"]["Message"]
        logging.error(
            f"ClientError occurred while uploading file to S3: {error_message}"
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file to S3: {error_message}",
        )

    except BotoCoreError as boto_err:
        logging.error(f"BotoCoreError occurred while using boto3: {str(boto_err)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while uploading the file to S3.",
        )

    except Exception as general_err:
        logging.exception(f"Unexpected error during file upload: {str(general_err)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while uploading the file to S3.",
        )
