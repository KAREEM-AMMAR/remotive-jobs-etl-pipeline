import psycopg2
import requests

# Database connection settings based on the Docker configuration
DB_HOST = "postgres"
DB_PORT = "5432"
DB_NAME = "data_warehouse"
DB_USER = "root"
DB_PASS = "rootpassword"

# Remotive API URL to fetch remote data jobs
API_URL = "https://remotive.com/api/remote-jobs?category=data&limit=20"


def run_extraction():
    print("🚀 [IBM ETL] Starting data extraction from Remotive API...")

    response = requests.get(API_URL)

    # Ensure the connection succeeded and status code is 200
    if response.status_code != 200:
        print(f"❌ Failed to connect to API. Status code: {response.status_code}")
        return

    # Convert incoming data to JSON format
    data = response.json()

    # Extract the jobs list from the data dictionary
    jobs = data.get("jobs", [])
    print(f"✅ Successfully fetched {len(jobs)} jobs from the source.")

    # Connect to PostgreSQL database and load data into staging table
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
        )
        cursor = conn.cursor()

        # SQL query to insert data into staging table
        insert_query = """
            INSERT INTO staging_jobs (job_id, title, company_name, category, publication_date, url, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        # Loop through each fetched job and insert it
        for job in jobs:
            cursor.execute(
                insert_query,
                (
                    str(job.get("id")),
                    job.get("title"),
                    job.get("company_name"),
                    job.get("category"),
                    str(job.get("publication_date")),
                    job.get("url"),
                    job.get("description"),
                ),
            )

        # Permanently commit changes to the database
        conn.commit()
        print(f"🎉 [Success] Saved {len(jobs)} records into staging_jobs table successfully!")

    except Exception as e:
        print(f"❌ An error occurred while connecting or inserting to DB: {e}")

    finally:
        # Close cursor and connection to preserve system resources
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    run_extraction()