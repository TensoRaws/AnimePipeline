from pydantic import BaseModel, FilePath


class FileNameInfo(BaseModel):
    path: FilePath
    episode: int
    name: str
    uploader: str
