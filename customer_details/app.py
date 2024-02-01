"""Customer Details MicroService."""
import os
import json
import uvicorn
import requests
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/")
async def submit_form(
    name: str = Form(...),
    phone_number: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
):
    """Handle the form submission.

    Args:
        name (str): The name from the form.
        phone_number (str): The phone number from the form.
        email (str): The email from the form.
        address (str): The address from the form.

    Returns:
        dict: JSON response after form submission.
    """
    base_url = os.getenv('BASE_URL', 'http://localhost') + ':' + os.getenv(
        'DAPR_HTTP_PORT', '3500'
    )
    headers = {'dapr-app-id': 'order-processor', 
               'content-type': 'application/json'}
    order = {
        'name': name,
        'contact': [
            {
                'phone_number': phone_number,
                'email': email,
                "address": address
            }
        ]
    }
    response = requests.post(
        url='%s/orders' % (base_url),
        data=json.dumps(order),
        headers=headers
    )
    
    
    return {"status": "success", "message": "Form submitted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, port=8020)
