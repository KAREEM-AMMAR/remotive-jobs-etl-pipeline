import psycopg2

# Database connection settings in Docker
DB_HOST = "postgres"
DB_PORT = "5432"
DB_NAME = "data_warehouse"
DB_USER = "root"
DB_PASS = "rootpassword"

def run_transformation():
    print("🔄 [IBM ETL] Starting data transformation and cleaning process...")
    
    try:
        # Open connection to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        print("✅ Connected to the database successfully.")
        
        # Fetch raw data from the staging table
        cursor.execute("SELECT job_id, title, company_name, category, publication_date, url, description FROM staging_jobs;")
        raw_jobs = cursor.fetchall()
        
        print(f"📊 Fetched {len(raw_jobs)} records from staging_jobs for transformation.")

        # Insert query into the cleaned transformed table
        insert_transformed_query = """
            INSERT INTO transformed_jobs (job_id, title, company_name, category, publication_date, url, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (job_id) DO NOTHING; -- Avoid duplicate entries if script runs multiple times
        """
        
        transformed_count = 0
        
        # Process and clean each record individually
        for job in raw_jobs:
            # Tuple unpacking to distribute columns into clear variables
            job_id, title, company_name, category, publication_date, url, description = job
            
            # Basic cleaning operations (strip whitespace or handle null values)
            clean_title = title.strip() if title else "Untitled"
            clean_company = company_name.strip() if company_name else "Unknown Company"
            clean_category = category.strip() if category else "General"
            
            parsed_date = publication_date

            # Execute insert for the cleaned table
            cursor.execute(
                insert_transformed_query,
                (
                    job_id,
                    clean_title,
                    clean_company,
                    clean_category,
                    parsed_date,
                    url,
                    description
                )
            )
            transformed_count += 1

        # Permanently commit changes to the database
        conn.commit()
        print(f"🎉 [Success] Successfully transformed and loaded {transformed_count} records into transformed_jobs table!")

    except Exception as e:
        print(f"❌ An error occurred during the transformation phase: {e}")
        if 'conn' in locals():
            conn.rollback() # Rollback changes if an error occurs

    finally:
        # Close resources to preserve system resources
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    run_transformation()