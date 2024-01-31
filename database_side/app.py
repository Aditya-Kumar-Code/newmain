from fastapi import FastAPI,Request,HTTPException
from dapr.ext.fastapi import DaprApp
import pydantic
from typing import List

class address(pydantic.BaseModel):
    phone_number:str
    email:str
    address:str
    @pydantic.validator("phone_number")
    def validate_phone_number(cls, v):
        if len(v) != 10:
            print("Invalid phone number format")
            raise ValueError("Invalid phone number format")
            
        return v
    @pydantic.validator("address")
    def validate_email(cls, v):
        if len(v)<=5:
            print("Too Short Address")
            return ValueError("Too short address")
            
        if len(v)>=200:
            print("Too Long Address")
            raise ValueError("Too long address")
        return v
    
class customer_details(pydantic.BaseModel):
    
    name:str
    contact:List[address]

    @pydantic.validator("contact", each_item=True, pre=True)
    def validate_contact(cls, value):
        return address(**value)


    @pydantic.validator("contact")
    
    def validate_contact_list_length(cls, v):
        if len(v) < 1:
            raise ValueError("At least one contact must be provided")
        return v
    
    
    

    
import json
app=FastAPI()
darp_app=DaprApp
@app.post('/orders')
async def getOrder(request:Request):
    data=await request.body()
    
    # print(data.decode('ASCII'))
    try:
        
        u=(data.decode('ASCII'))
        res = json.loads(u)
        validated_data = customer_details(**res)

        print(validated_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {'ContentType': 'application/json'}
import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8001)
