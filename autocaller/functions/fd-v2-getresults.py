import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    print(event)

    

    dynamo = boto3.resource('dynamodb')

    tabl = dynamo.Table('caller_data')

    response = tabl.scan(FilterExpression=Attr("agentIdentifier").eq(event["agentIdentifier"])) # To get the results from dynamo db
    
    print(response)
    return {
        'statusCode': 200,
        'body': response["Items"]
    }
