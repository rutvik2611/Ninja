from fastapi import FastAPI
from optimus_db.secure_rsa_db.fetch_latest_rsa import fetch_valid_rsa_value
from optimus_db.secure_rsa_db.insert_secure_rsa import add_secure_rsa
from optimus_db.secure_rsa_db.update_status import update_attempt_status_and_html

app = FastAPI()

@app.get("/rsa")
def get_rsa():
    try:
        rsa_value = fetch_valid_rsa_value()
        return {"rsa_value": rsa_value}
    except Exception as e:
        return {"error": str(e)}

@app.post("/rsa/{rsa_value}")
def post_rsa(rsa_value: str):
    try:
        add_secure_rsa(rsa_value)
        return {"message": "RSA value added successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.put("/status/{status}")
def update_status(status: str):
    try:
        update_attempt_status_and_html(status)
        return {"message": "Status updated successfully"}
    except Exception as e:
        return {"error": str(e)}