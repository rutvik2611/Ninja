import sys
from pathlib import Path



sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from automation.trigger import trigger



from optimus_db.secure_rsa_db.fetch_latest_rsa import fetch_valid_rsa_value
from optimus_db.secure_rsa_db.insert_secure_rsa import add_secure_rsa
from optimus_db.secure_rsa_db.update_status import update_attempt_status

app = FastAPI()

@app.get("/rsa")
def get_rsa():
    try:
        rsa_value = fetch_valid_rsa_value()
        return {"rsa_value": rsa_value}
    except Exception as e:
        return {"error": str(e)}

@app.get("/rsa/{rsa_value}")
def post_rsa(rsa_value: int):
    try:
        if rsa_value is not None:
            try:
                add_secure_rsa(rsa_value)
                trigger()
                update_attempt_status(new_status="success")
                comment ="RSA value added successfully"
            except Exception as e:
                print(f"An error occurred: {e}")
                update_attempt_status(new_status="failure",msg=str(e))
                comment = "RSA value added successfully, but trigger failed: " + str(e)
        return {"message": comment}
    except Exception as e:
        return {"error": str(e)}

@app.put("/status/{status}")
def update_status(status: str):
    try:
        update_attempt_status(status)
        return {"message": "Status updated successfully"}
    except Exception as e:
        return {"error": str(e)}