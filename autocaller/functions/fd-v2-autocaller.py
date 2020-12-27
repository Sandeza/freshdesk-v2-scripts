import json
import boto3

connect_client = boto3.client('connect')

client = boto3.resource('dynamodb')


table = client.Table("caller_data")



def connect_outbound_api(data):
    
    try:
        response = connect_client.start_outbound_voice_contact(
        DestinationPhoneNumber=data["phoneNumber"],
        SourcePhoneNumber="+18336624150",
        ContactFlowId=data['contactFlowId'],
        InstanceId=data['instanceId'],
        Attributes={
            'Message': data['message']
        })
        return {"id":response["ContactId"]}
        
    except Exception as e:
        print(e)
        return {"error":e}
            
    
    

        
    

    

def lambda_handler(event, context):
    print(json.dumps(event))
  
    agentIdentifier = event["agentIdentifier"]
    jobKey =  event["jobKey"]
    
    for val in jobKey:
        print(val)
        response = table.get_item(
    Key={
        "agentIdentifier": agentIdentifier,
        "jobKey":  val
    },
    AttributesToGet=[
        'message','phoneNumber','contactFlowId','instanceId'
    ] )
        print(response)
        call = connect_outbound_api(response['Item'])
        print(call)
        status = "Call Placed" if call.get("error")== None else call.get("error")
        table.update_item(
  Key={
    "agentIdentifier": agentIdentifier,
        "jobKey":  val
  },
  UpdateExpression='SET #ts = :val1',
  ExpressionAttributeValues={
    ":val1": str(status)
  },
  ExpressionAttributeNames={
    "#ts": "status"
  }
)

        table.update_item(
  Key={
 "agentIdentifier": agentIdentifier,
        "jobKey":  val
  },
  UpdateExpression='SET #ts = :val1',
  ExpressionAttributeValues={
    ":val1": str(call.get("id"))
  },
  ExpressionAttributeNames={
    "#ts": "contactId"
  }
)

        
    
    
    
    
   
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
