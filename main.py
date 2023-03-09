from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
import os

import uvicorn


@app.get("/")
async def root():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Fancy Surface Reconstruction (vtk copy paste) 🐋</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_level="info"
    )
