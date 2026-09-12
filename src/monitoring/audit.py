from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from src.utils.logger import logger
import os
from datetime import datetime

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)


def start_pipeline_run():

    try:
        logger.info("Creating pipeline audit record")

        start_time = datetime.now()

        with engine.begin() as connection:

            result = connection.execute(
                text("""
                    INSERT INTO pipeline_runs
                    (start_time, status)
                    VALUES (:start_time, :status)
                    RETURNING run_id
                """),
                {
                    "start_time": start_time,
                    "status": "RUNNING"
                }
            )

            run_id = result.scalar()

        logger.info(f"Pipeline audit run created: {run_id}")

        return run_id

    except Exception as e:

        logger.error(f"{e} occurred while creating pipeline audit record")
        raise


def finish_pipeline_run(
    run_id,
    status,
    rows_extracted,
    rows_loaded
):

    try:
        logger.info(f"Updating pipeline audit record: {run_id}")

        end_time = datetime.now()

        with engine.begin() as connection:

            connection.execute(
                text("""
                    UPDATE pipeline_runs
                    SET
                        end_time = :end_time,
                        status = :status,
                        rows_extracted = :rows_extracted,
                        rows_loaded = :rows_loaded
                    WHERE run_id = :run_id
                """),
                {
                    "run_id": run_id,
                    "end_time": end_time,
                    "status": status,
                    "rows_extracted": rows_extracted,
                    "rows_loaded": rows_loaded
                }
            )

        logger.info(f"Pipeline audit record updated: {run_id}")

    except Exception as e:

        logger.error(f"{e} occurred while updating pipeline audit record")
        raise