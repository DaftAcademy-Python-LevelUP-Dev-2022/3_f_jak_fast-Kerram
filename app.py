import datetime

from dateutil.relativedelta import relativedelta
from fastapi import Depends, FastAPI, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse
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


@app.get("/info")
def info(request: Request, format: str = ""):
    if format == "json":
        return {
            "user_agent": f"{request.headers['User-Agent']}"
        }
    elif format == "html":
        return HTMLResponse(f"""
        <input type="text" id=user-agent name=agent value="{request.headers['User-Agent']}">
        """)
    else:
        return Response(status_code=400)


paths_used = set()


@app.put("/save/{string}")
def save(string: str):
    paths_used.add(string)
    return Response(status_code=200)


@app.get("/save/{string}")
def save(string: str):
    if string in paths_used:
        return RedirectResponse("/info", status_code=301)
    else:
        return Response(status_code=404)


@app.delete("/save/{string}")
def save(string: str):
    paths_used.remove(string)
    return Response(status_code=200)


@app.post("/save/{string}")
@app.options("/save/{string}")
@app.head("/save/{string}")
@app.trace("/save/{string}")
@app.patch("/save/{string}")
def save(string: str):
    return Response(status_code=400)
