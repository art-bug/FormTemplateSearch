import pytest
import requests

test_fields = [
        ({
            "arrived": "22.07.2021"
         },
         {
            "arrived": "DATE"
        }),
        ({
            "arrival": "2021-07-22"
         },
         {
            "arrival": "DATE"
        }),
        ({
            "arrival": "22.07.2021"
         },
         {
            "form": "OrderForm"
        }),
        ({
            "first_name": "Сергей",
            "phone": "+7 999 999 99 99",
            "email": "sergey_ivanov@gmail.com"
         },
         {
            "form": "ContactForm"
        }),
        ({
            "first_name": "Иван",
            "phone": "+7 999 999 99 99",
            "email": "sergey_ivanov@gmail.com"
         },
         {
            "first_name": "TEXT",
            "phone": "PHONE",
            "email": "EMAIL"
        }),
        ({
            "employee_name": "Сергей",
         },
         {
            "form": "EmployeeForm"
        })
]

@pytest.mark.parametrize("fields, expected_response", test_fields)
def test_request(fields, expected_response):
    response = requests.post("http://localhost:8000/get_form", params=fields)
    response = response.json()
    assert response == expected_response

