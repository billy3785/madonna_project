from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Madonna Project API is running!"}

@app.get("/events")
def get_events():
    return {"data": "Events will be listed here"}

@app.get("/people")
def get_people():
    return {"data": "People involved will be listed here"}