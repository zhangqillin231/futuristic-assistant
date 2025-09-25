
# backend/routes/train.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os, tempfile, shutil
from ..train_pipeline import index_folder

router = APIRouter(prefix='/train')

class TrainResponse(BaseModel):
    status: str
    indexed_chunks: int | None = None

@router.post('/upload')
async def upload_and_train(file: UploadFile = File(...)):
    # Expect a zip of txt files or a single txt
    tmpdir = tempfile.mkdtemp()
    try:
        contents = await file.read()
        filepath = os.path.join(tmpdir, file.filename)
        with open(filepath, 'wb') as f:
            f.write(contents)
        # If zip, extract
        if file.filename.endswith('.zip'):
            import zipfile
            with zipfile.ZipFile(filepath, 'r') as z:
                z.extractall(tmpdir)
            folder_to_index = tmpdir
        else:
            # assume text file
            folder_to_index = tmpdir
        index_folder(folder_to_index)
        return JSONResponse({'status': 'ok'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
