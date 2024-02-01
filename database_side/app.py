"""Database side microservice."""
import json
import uvicorn
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel, Field, ValidationError, validator

class ContactDetails(BaseModel):
    """Pydantic model for contact details.

    Attributes:
        phone_number (str): The phone number.
        email (str): The email address.
        address (str): The address.
    """
    phone_number: str = Field(..., min_length=10, max_length=10)
    email: str = Field(..., min_length=2, max_length=30)
    address: str = Field(..., min_length=6, max_length=200)

class CustomerDetails(BaseModel):
    """Pydantic model for customer details.

    Attributes:
        name (str):
                 The customer's name.
        contact (List[ContactDetails]): 
                List of contact details for the customer.
    """
    name: str = Field(..., min_length=2, max_length=20)
    contact: list[ContactDetails]

    @validator("contact", pre=True, each_item=True)
    def validate_contact(cls, value):
        """Validating contact."""
        return ContactDetails(**value)

app = FastAPI()
dapr_app = DaprApp(app)

@app.post("/orders")
async def get_order(customer_details_request: Request):
    """Handle the incoming order request.

    Args:
        customer_details_request (Request): 
                The FastAPI request object containing customer details.

    Returns:
        dict: A response indicating the content type.
    """
    try:
        data = await customer_details_request.body()
        u = data.decode("ASCII")
        "loads json data"
        res = json.loads(u)
        
        try:
            validated_data = CustomerDetails(**res)
            with open('data.json', 'w') as json_file:
                json.dump(validated_data, json_file, indent=2)

            print("Customer details saved successfully")
        except ValidationError as model_validation_error:
            print(model_validation_error)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=str(e))

    return {"Message": "Got the response"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
