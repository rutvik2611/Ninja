import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path



sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from automation.trigger import trigger



from optimus_db.secure_rsa_db.fetch_latest_rsa import fetch_valid_rsa_value
from optimus_db.secure_rsa_db.insert_secure_rsa import add_secure_rsa
from optimus_db.secure_rsa_db.update_status import update_attempt_status

from optimus_db.r743189.r743189_db import fetch_valid_rsa_postgres

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
                with ThreadPoolExecutor() as executor:

                    future1 = executor.submit(trigger, secure_id=rsa_value)
                    future2 = executor.submit(add_secure_rsa, rsa_value)
                    # Get the results of the tasks to raise any exceptions
                    future1.result()
                    future2.result()
                update_attempt_status(new_status="success")
                comment ="RSA value added successfully"
            except Exception as e:
                print(f"An error occurred in post_rsa: {e}")
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

@app.get("/auto")
def post_rsa2():
    try:
        rsa_value = fetch_valid_rsa_postgres()
        if rsa_value is not None:
            try:
                with ThreadPoolExecutor() as executor:


                    future1 = executor.submit(trigger, secure_id=rsa_value)
                    future2 = executor.submit(add_secure_rsa, rsa_value)
                    # Get the results of the tasks to raise any exceptions
                    future1.result()
                    future2.result()
                update_attempt_status(new_status="success")
                comment ="RSA value added successfully"
            except Exception as e:
                print(f"An error occurred in post_rsa: {e}")
                update_attempt_status(new_status="failure",msg=str(e))
                comment = "RSA value added successfully, but trigger failed: " + str(e)
        return {"message": comment}
    except Exception as e:
        return {f"RSA:{rsa_value} error": str(e)}