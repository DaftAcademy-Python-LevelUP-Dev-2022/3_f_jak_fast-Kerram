from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/start", response_class=HTMLResponse)
def start():
    return """
    <h1>The unix epoch started at 1970-01-01</h1>
    """
