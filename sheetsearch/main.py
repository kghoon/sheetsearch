
import json
import tempfile
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.params import Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from sheetsearch import chatgpt, google, config, pdfutil


app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("static/pages/index.html", headers={'Cache-Control': 'no-cache'})


@app.get("/api/search")
async def search(search: str):
    print(f"search={search}")

    result = google.search_images(search)
    print(json.dumps(result, indent=4))

    return result


class SongAnalyzeRequest(BaseModel):
    prompt: str

@app.post("/api/analyze_songlist")
async def analyze_songlist(req: SongAnalyzeRequest):
    prompt = f'''
아래 글에서 노래 제목과 조성(Key)를 찾아서 csv로 만들어줘.
헤더 필드명은 title,key로 해줘. csv만 출력해줘.

아래와 같은 형식으로 출력해줘
title,key
예수나를위하여,D
경배하리,C

아래 글에서 찾아줘

{req.prompt}
'''

    print(f"prompt={prompt}")

    result = chatgpt.query(prompt)

    return result



class PdfGenerateRequest(BaseModel):
    filelist: List[str]


async def get_temp_dir():
    dir = tempfile.TemporaryDirectory()
    try:
        yield dir.name
    finally:
        del dir


@app.post("/api/generate_pdf")
async def generate_pdf_file(req: PdfGenerateRequest, dir=Depends(get_temp_dir)):

    local_filelist = pdfutil.download_imagefiles(req.filelist, dir)
    result = pdfutil.generate_pdf(local_filelist, dir)

    return FileResponse(result, media_type="application/pdf", filename=result, headers={'Cache-Control': 'no-store'})


class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path, *args, **kwargs):
        response = await super().get_response(path, *args, **kwargs)
        response.headers["Cache-Control"] = "no-cache"
        return response


app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")


def main():
    port = config.PORT
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
