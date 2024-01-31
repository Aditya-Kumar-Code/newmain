from fastapi import FastAPI,Request,HTTPException
from dapr.ext.fastapi import DaprApp
import pydantic
from typing import List

class address(pydantic.BaseModel):
    phone_number:str
    email:str
    address:str
    
class customer_details(pydantic.BaseModel):
    
    name:str
    contact:List[address]
    
    
    

    
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
        
        with open('orders..txt', 'w') as output:
                output.write(u)
        print(validated_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {'ContentType': 'application/json'}
import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8001)
