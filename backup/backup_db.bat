@echo off

:: Set your database credentials
set PG_USER=gopal
set PG_PASSWORD=gopal
set PG_DB=fastapi_resume_upload_aws
set PG_HOST=localhost
set PG_PORT=5432
set BACKUP_DIR=D:\professional\resume_upload_Fastapi\backup

:: Generate timestamp
set TIMESTAMP=%DATE%_%TIME%
set TIMESTAMP=%TIMESTAMP: =0%
set TIMESTAMP=%TIMESTAMP:/=-%
set TIMESTAMP=%TIMESTAMP::=-%

:: Set the backup file name with timestamp
set BACKUP_FILE=%BACKUP_DIR%\backup_%TIMESTAMP%.dump

:: Set the password for pg_dump utility
set PGPASSWORD=%PG_PASSWORD%

:: Run pg_dump to take the backup
pg_dump -U %PG_USER% -h %PG_HOST% -p %PG_PORT% -F c -b -v -f %BACKUP_FILE% %PG_DB%

:: Clear the password environment variable
set PGPASSWORD=

echo Backup completed and saved to %BACKUP_FILE%
pause
