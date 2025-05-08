import json
import boto3
import logging
import datetime
import psycopg2


logger=logging.getLogger()
logger.setLevel(logging.INFO)

def fetch_records():
    list_of_records = [
        {'Id': 1, 'firstName': 'Ashutosh', 'lastName': 'Satapathy'},
        {'Id': 2, 'firstName': 'Ronnie', 'lastName': 'Satapathy'},
        {'Id': 3, 'firstName': 'Kamal', 'lastName': 'Lochan'},
        {'Id': 4, 'firstName': 'Sabyasachi', 'lastName': 'Jr.'},
        {'Id': 5, 'firstName': 'Amitabh', 'lastName': 'Patnaik'},
        {'Id': 6, 'firstName': 'Nihar', 'lastName': 'Das'},
        {'Id': 7, 'firstName': 'Sumit', 'lastName': 'Mohanty'},
        {'Id': 8, 'firstName': 'Prachi', 'lastName': 'Mishra'},
        {'Id': 9, 'firstName': 'Rashmita', 'lastName': 'Behera'}
    ]  
    return list_of_records

def filter_records(records, **criteria):
    return [record for record in records if all(record.get(key) == value for key, value in criteria.items())]

def connect_to_DB():
    try:
        conn = psycopg2.connect(
            host="policy-poc.cluster-clzfvi53z3dr.us-east-1.rds.amazonaws.com",
            database="policy-poc",
            user="postgres",
            password="postgres",
            port=5432
        )
        logger.info("Connected to PostgreSQL")

        cur = conn.cursor()
        query= """
            CREATE TABLE policy_poc (
                policyId INT PRIMARY KEY AUTO_INCREMENT,  -- Unique identifier for the policy
                servicerOrgNumber VARCHAR(50) NOT NULL,   -- Organization number associated with the policy
                status VARCHAR(20) NOT NULL,              -- Status of the policy (e.g., Active, Pending, Closed)
                policyName VARCHAR(100),                  -- Name of the policy
                createdDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when record was created
                updatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- Last updated timestamp
            );
         """
        cur.execute(query)
        # rows = cur.fetchall()
        # logger.info(f"Fetched {len(rows)} rows")

        cur.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": rows  # You might need to serialize rows to JSON
        }

    except Exception as e:
        raise e


s3=boto3.client('s3')
def lambda_handler(event, context):
    try:
        connect_to_DB()
        # logger.info(f"Input Event is {json.dumps(event)}")
        # logger.info("Started uploading file to S3")
        # currentDateTime=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        # logger.info(f"Successfully added Date time {currentDateTime}")
        # bucket='enact-prac-sqs'
        # result = fetch_records()
        # logger.info(f"Result is {result}")
        # logger.info(f"Criteria is {json.dumps(event)}")
        # fileToUpload = filter_records(result, **event)

        # logger.info(f"Filtering completed {fileToUpload}")
        # logger.info("Filtering completed")
        # fileName='Ronnie'+ str(currentDateTime) +  '.json'
        # logger.info(f"File Name is ',{fileName}")
        # uploadByteStream=bytes(json.dumps(fileToUpload).encode('UTF-8'))
        # s3.put_object(Bucket=bucket,Key='TEMP/'+fileName,Body=uploadByteStream)
        # logger.info('Upload Completed Successfully')

    except Exception as e:
        logger.error(f"Something went wrong {e}")
        raise e
    
