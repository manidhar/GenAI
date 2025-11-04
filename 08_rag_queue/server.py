from fastapi import FastAPI, Body,Query
from .client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server is up and running."}


@app.post("/chat")
def chat(query:str=Query(...,description="The chat query of the user")):

    job=queue.enqueue(process_query,query)
    return {"stauts":"queued","job_id":job.get_id()}

@app.get("/job-status")
def get_result(job_id:str=Query(...,description="The Job ID to fetch result for")):
    job=queue.fetch_job(job_id)
    result=job.return_value()

    return {"status":job.get_status(),"result":result}
    