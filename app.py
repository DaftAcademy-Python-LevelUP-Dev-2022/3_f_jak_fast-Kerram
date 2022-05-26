import datetime

from dateutil.relativedelta import relativedelta
from fastapi import Depends, FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()


@app.get("/start", response_class=HTMLResponse)
def start():
    return """
    <h1>The unix epoch started at 1970-01-01</h1>
    """


@app.post("/check", response_class=HTMLResponse)
def check(credentials: HTTPBasicCredentials = Depends(security)):
    date_str = credentials.password
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return Response(status_code=401)

    # Taken from https://stackoverflow.com/questions/4436957/pythonic-difference-between-two-dates-in-years.
    age = relativedelta(datetime.datetime.now(), date).years
    if age < 16:
        return Response(status_code=401)

    return f"""
    <h1>Welcome {credentials.username}! You are {age}</h1>
    """
