from tinydb import TinyDB, Query
from fastapi import FastAPI, Request
from validator_chain import DateValidator, PhoneValidator, EmailValidator

app = FastAPI()

formtemplates = TinyDB("formtemplates.json", indent=4, separators=(',', ': '))

FormTemplate = Query()

validation_chain = DateValidator()
validation_chain.set_next(PhoneValidator()).set_next(EmailValidator())

@app.get("/")
async def index():
    return {"status": "success"}

async def validate(field_value: str):
    return validation_chain.validate(field_value)

@app.post("/get_form")
async def get_form(request: Request):
    response = {}

    form_fields = dict(request.query_params)

    search_result = formtemplates.get(FormTemplate.fragment(form_fields))

    if not search_result:
        response = {field:await validate(value) for field, value in form_fields.items()}

        return response

    response["form"] = search_result["name"]

    return response

