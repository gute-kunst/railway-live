import aiofiles
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

from algorithm import surface_pipeline

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
            <form action="/reconstruction/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="number" placeholder="cell size" name="cellsize" step="any" min=0 max=1/>
                <input type="submit">

            </form> 
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


INPUT_FILE_PATH = "./tmp/pc.vtp"
OUTPUT_FILE_PATH = "./tmp/surface.stl"


@app.post("/reconstruction/")
async def create_upload_file(file: UploadFile, cellsize: float = Form()):
    if not os.path.isdir("tmp"):
        os.makedirs("tmp")
    async with aiofiles.open(INPUT_FILE_PATH, "wb") as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
    surface_pipeline(INPUT_FILE_PATH, OUTPUT_FILE_PATH, cellsize)
    return FileResponse(OUTPUT_FILE_PATH, filename="surface.stl", media_type="binary")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_level="info"
    )
