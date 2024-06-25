import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime, timezone

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
        post_rsa = fetch_valid_rsa_postgres()
        return {"sql_rsa_value": rsa_value,
                "postgres_rsa_value": post_rsa[0]}
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
    rsa_value=0
    try:
        rsa_value,date_time = fetch_valid_rsa_postgres()
        rsa = rsa_value
        length = len(str(rsa))
        if length < 8:
            append = 8 - length

            rsa = '0' * append + str(rsa)


        # Get the current datetime
        now = datetime.now(timezone.utc)

        # Calculate the difference in seconds
        difference = (now - date_time.replace(tzinfo=timezone.utc)).total_seconds()

        # Check if the difference is less than 60 seconds
        print(f"Difference: {difference}")
        if difference < 60:
            print("The datetime is less than 60 seconds old.")
            if rsa_value is not None:
                rsa = rsa_value
                length = len(str(rsa))
                if length < 8:
                    append = 8 - length

                    rsa = str('0' * append + str(rsa))
                    print(type(rsa))
                    rsa_value = rsa
                try:
                    with ThreadPoolExecutor() as executor:

                        future1 = executor.submit(trigger, secure_id=rsa_value)
                        future2 = executor.submit(add_secure_rsa, rsa_value)
                        # Get the results of the tasks to raise any exceptions
                        future1.result()
                        future2.result()
                    update_attempt_status(new_status="success")
                    comment = f"RSA {rsa_value} added successfully, which was {difference} seconds old."
                except Exception as e:
                    print(f"An error occurred in post_rsa: {e}")
                    update_attempt_status(new_status="failure", msg=str(e))
                    comment = "RSA value added successfully, but trigger failed: " + str(e) + f" for {rsa_value}"
            return {"message": comment}
        else:
            print(f"More than 60s old. and date_time: {date_time} and now: {now} so {difference} for {rsa_value}")

            raise ValueError(f"It's {difference} seconds old so not triggering to log you in automatically.")

    except Exception as e:
        if rsa_value != 0:
            return {f"RSA: error for {rsa_value}": str(e)}
        return {"Could Not get RSA": str(e)}