import json
import boto3 
import os
from random import randint
from boto3.dynamodb.conditions import Key, Attr
import datetime

client = boto3.resource('dynamodb')


table = client.Table("caller_data")

function = boto3.client('lambda')

def lambda_handler(event, context):
    print(event)

    data1 = event
    data = json.loads(data1["body"])
            

    txt = []
    i=0
    
    for val in data["phoneNumbers"] :
        print(val)
        jobKey = str(randint(100000, 999999))
    
        txt.append(jobKey)
         
        
        table.put_item(Item= {'agentIdentifier': data["agentIdentifier"],'jobKey':  jobKey,
        "contactFlowId":data["contactFlowId"],"instanceId":data["instanceId"]
            ,"dateTime":str(datetime.datetime.utcnow()),"phoneNumber":val,"message":data["message"]})
        i+=1
    
    response = function.invoke_async(
    FunctionName='connectPing',
    InvokeArgs=json.dumps({"agentIdentifier":data['agentIdentifier'],"jobKey":txt}))
    print(response)
  
    




    
        
        
        

    return {
        'statusCode': 200,
        'body': json.dumps("Call Placed")
    }
