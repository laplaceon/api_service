from fastapi import FastAPI
from pydantic import BaseModel
import logging
import asyncio
import requests

# Define FastAPI app
app = FastAPI()

class LogData(BaseModel):
    logs: list

@app.post("/log-analysis/")
async def log_analysis(log_data: LogData):
    url = 'https://api.github.com/repos/tousif101/api_service/issues'
    headers = {'Authorization': 'token PUT_TOKEN_HERE'}
    issue_title = '🔎 Anomaly Detected in Logs'
    issue_created = False
    issue_count = 0

    for log in log_data.logs:
        if "400" in log or "500" in log:
            issue_body = "An anomaly was detected in the logs. Here's an example: " + log
            payload = {'title': issue_title, 'body': issue_body}
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                issue_created = True
                issue_count += 1

    if issue_created:
        return {"status": f"Successfully created {issue_count} GitHub Issue(s)"}
    else:
        return {"status": "No anomalies detected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
