from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

DATABASE_URL = "dbname=fall_detection_uwzd user=fall_detection_uwzd_user password=TSFtnTEpJMS02re7dsRMm6YFeTV107JI host=dpg-cp41st779t8c73e98fkg-a.singapore-postgres.render.com port=5432"

# Allow CORS for all origins during development (replace "*" with your actual frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class SensorData(BaseModel):
    acceleration: float
    gyroscope: float

@app.post("/sensor")
async def add_sensor_data(sensor_data: SensorData):
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Get current datetime
        now = datetime.now()

        # Insert sensor data and current datetime into the table
        cur.execute(
            """
            INSERT INTO falldetect (acceleration, gyroscope)
            VALUES (%s, %s)
            """,
            (sensor_data.acceleration, sensor_data.gyroscope)
        )

        # Commit the transaction
        conn.commit()

        return {"status": "success"}

    except psycopg2.Error as e:
        return {"status": "error", "detail": str(e)}

    finally:
        # Close communication with the database
        if conn:
            cur.close()
            conn.close()
