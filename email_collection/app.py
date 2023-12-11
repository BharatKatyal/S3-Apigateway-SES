import json
import boto3
import os
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['USER_DATA_TABLE'])
ses = boto3.client('ses', region_name=os.environ['SES_REGION'])
source_email = os.environ['SES_SOURCE_EMAIL']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    
    first_name = body.get('first_name', '')
    email = body.get('email', '')
    
    if not first_name or not email:
        return {
            'statusCode': 400,
            'body': json.dumps('Both first_name and email are required.')
        }
    
    try:
        # Store data in DynamoDB
        table.put_item(Item={'email': email, 'first_name': first_name})
        
        # Send an email to the user's provided email address
        response = ses.send_email(
            Source=source_email,
            Destination={
                'ToAddresses': [email]  # Use the user's provided email as the destination
            },
            Message={
                'Subject': {
                    'Data': 'Data Submitted'
                },
                'Body': {
                    'Text': {
                        'Data': f'First Name: {first_name}\nEmail: {email}'
                    }
                }
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data submitted successfully. An email has been sent to your provided email address...')
        }
    except Exception as e:
        # Log the error to CloudWatch Logs
        logger.error(f'Error: {str(e)}')
        
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
