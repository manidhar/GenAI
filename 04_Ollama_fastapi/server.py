from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/contact-us")
def contactus_root():
    return {"email": "manidhar.k@gmail.com"}