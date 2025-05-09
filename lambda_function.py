import json
import boto3
import logging
import datetime
import psycopg2


logger=logging.getLogger()
logger.setLevel(logging.INFO)


def connect_to_DB(event):
    try:
        logger.info("Started Connecting to PostgreSQL")

        conn = psycopg2.connect(
            host="proxy-1746712528059-policy-p3.proxy-clzfvi53z3dr.us-east-1.rds.amazonaws.com",
            database="policy_poc_2",
            user="postgres",
            password="postgres",
            port=5432
        )

        logger.info("Connected to PostgreSQL")

        cur = conn.cursor()
        query= """
            SELECT * FROM policy_search_load_test WHERE 1=1
         """
        if event.get('billingOrgNumber'):
            query += " AND servicer_org_nbr = '%s'"%event.get("billingOrgNumber")

        cur.execute(query)
        result = cur.fetchall()
        logger.info(f"Final query prepared as: {query}")
        logger.info(f"Fetched {len(result)} rows")

        cur.close()
        conn.close()
        
        return result


    except Exception as e:
        raise e

def build_response(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body:
        response['body'] = body
    return response


def prepare_response(result):
    try:
        logger.info("Started preparing response")
        column_names = ["policyNumber", "billingOrgNumber", "status"]
        json_ready = [
        {key: value for key, value in zip(column_names, row[:3])}
        for row in result
    ]
        logger.info(f"Successfully prepared response: {json_ready[0]}")
        return json_ready
    except Exception as e:
        logger.error(f"Something went wrong {e}")
        return build_response(500, json.dumps({"error": str(e)}))


s3=boto3.client('s3')
def lambda_handler(event, context):
    try:
        logger.info("Started execution")
        result=connect_to_DB(event)
        
        logger.info(f"Input Event is {json.dumps(event)}")
        billingOrgNumber=event.get('billingOrgNumber')
        logger.info(f"BillingOrgNumber is {billingOrgNumber}")
        logger.info("Started uploading file to S3")
        currentDateTime=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        logger.info(f"Successfully added Date time {currentDateTime}")
        bucket='enact-prac-sqs'
        # logger.info(f"Result is {result}")
        json_array=prepare_response(result)
        # json_array = [r[0] for r in result]
        logger.info(f"First Index of array is {json_array[0]}")
        
        fileName='policies'+ str(currentDateTime) +  '.json'
        logger.info(f"File Name is ',{fileName}")
        key='TEMP/'+fileName
        uploadByteStream=bytes(json.dumps(json_array).encode('UTF-8'))
        logger.info(f"Testing: {json_array[0]}")
        logger.info(f"Started uploading the file to S3 bucket {bucket} and path is {key} of size {len(json_array)}")
        s3.put_object(Bucket=bucket,Key=key,Body=uploadByteStream)
        logger.info('Upload Completed Successfully')
        finalRes={"bucket":bucket,"key":key}
        return build_response(200, json.dumps(finalRes))

    except Exception as e:
        logger.error(f"Something went wrong {e}")
        return build_response(500, json.dumps({"error": str(e)}))