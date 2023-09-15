from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import boto3

app = FastAPI()

aws_access_key_id = 'AKIAU4PD3WV4JBD25BZK'
aws_secret_access_key = '0uzhQna1Z175yz2schqM01aNoCIyWJxgMDqBHZGy'
aws_region = 'ap-south-1'  # Replace with your AWS region

# Initialize the DynamoDB client with the credentials
dynamodb = boto3.client('dynamodb', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_item/{item_id}")
async def get_item(item_id: str):
    try:
        response = dynamodb.get_item(
            TableName='mycutomerdetails',
            Key={'customerid': {'S': item_id}}
        )
        item = response.get('Item')
        if item:
            return {"message": "Item found", "data": item}
        else:
            return {"message": "Item not found"}
    except Exception as e:
        return {"message": "Error", "error": str(e)}


@app.put("/update_item/{item_id}")
async def update_item(item_id: str, update_data: dict):
    try:
        response = dynamodb.update_item(
            TableName='mycutomerdetails',
            Key={'customerid': {'S': item_id}},
            UpdateExpression='SET #attr1 = :val1, #attr2 = :val2',
            ExpressionAttributeNames={'#attr1': 'StudentName', '#attr2': 'City'},
            ExpressionAttributeValues={':val1': {'S': update_data['StudentName']}, ':val2': {'S': update_data['City']}},
            ReturnValues='UPDATED_NEW'
        )
        return {"message": "Item updated successfully", "response": response}
    except Exception as e:
        return {"message": "Error", "error": str(e)}


@app.post("/store_item/")
async def store_item(item_data: dict):
    try:
        response = dynamodb.put_item(
            TableName='mycutomerdetails',
            Item=item_data
        )
        return {"message": "Item stored successfully", "response": response}
    except dynamodb.exceptions.ClientError as e:
        return {"message": "DynamoDB Error", "error": str(e)}
    except Exception as e:
        return {"message": "Error", "error": str(e)}
    

@app.delete("/delete_item/{item_id}")
async def delete_item(item_id: str):
    try:
        response = dynamodb.delete_item(
            TableName='mycutomerdetails',
            Key={'customerid': {'S': item_id}}
        )
        return {"message": "Item deleted successfully", "response": response}
    except Exception as e:
        return {"message": "Error", "error": str(e)}

