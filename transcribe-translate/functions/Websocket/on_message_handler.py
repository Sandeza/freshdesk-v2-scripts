import json
import boto3
import os
import requests


dynamodb = boto3.client('dynamodb')
client = boto3.client('translate')


def handle(event, context):
    print(json.dumps(event['body']),"body")
    message = json.loads(event['body'])['message']
    action  = json.loads(event['body'])['actions']
    target = json.loads(event['body']).get('target')
    txt = ''
    
    if action == "agentReceivedCall":
        txt =  event['requestContext']['connectionId'] 
        
        requests.post(f"https://aei2wry09g.execute-api.us-east-1.amazonaws.com/new/add?contactId={message}&connectionId={txt}")

    elif action =="translate":
        response = client.translate_text(
    Text=message,
    SourceLanguageCode='auto', # or auto
    TargetLanguageCode=target)
        txt = {"type":"translate","message": response["TranslatedText"] } 
    else:
        txt ={"type":"transcribe","message": message }

        
        

    print(event['requestContext']['connectionId'])
    try:
        
        connectionIds = []

        apigatewaymanagementapi = boto3.client('apigatewaymanagementapi', 
        endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])
        apigatewaymanagementapi.post_to_connection(
                Data=json.dumps(txt),
                ConnectionId=event['requestContext']['connectionId']
            )

        # Retrieve all connectionIds from the database
       

        # Emit the recieved message to all the connected devices
        
           
    except Exception as e:

        print(e)

    return {}