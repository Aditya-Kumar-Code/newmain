from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import requests
import json
import os
app = FastAPI()

# Configure templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/submit_form/")
async def submit_form(name: str=Form(...),phone_number: str=Form(...),email: str=Form(...),address: str=Form(...)):
    base_url = os.getenv('BASE_URL', 'http://localhost') + ':' + os.getenv(
                        'DAPR_HTTP_PORT', '3500')
    headers = {'dapr-app-id': 'order-processor', 'content-type': 'application/json'}
    order = {
            
            
            'name':name,
            'contact':
            [
                {
                'phone_number':phone_number,
                    'email':email,
                    "address":address
                }
            ]
            
            
    }
    requests.post(
        url='%s/orders' % (base_url),
            data=json.dumps(order),
            headers=headers
    )
    return  {name:'name'}

import uvicorn
uvicorn.run(app,port=8020)
