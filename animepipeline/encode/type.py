from typing import List, Optional

from pydantic import BaseModel


class TaskNotCompletedError(Exception):
    """
    Exception raised when a task is not completed yet.
    """

    def __init__(self, message: str = "Task not completed yet") -> None:
        self.message = message
        super().__init__(self.message)


class Error(BaseModel):
    message: str


class PingResponse(BaseModel):
    error: Optional[Error] = None
    success: bool


class NewTaskRequest(BaseModel):
    video_key: str


class NewTaskResponse(BaseModel):
    error: Optional[Error] = None
    success: bool


class StartTaskRequest(BaseModel):
    encode_param: str
    script: str
    video_key: str


class StartTaskResponse(BaseModel):
    error: Optional[Error] = None
    success: bool


class GetTaskProgressRequest(BaseModel):
    video_key: str


class GetTaskProgressResponse(BaseModel):
    class Data(BaseModel):
        class Progress(BaseModel):
            clip_key: str
            clip_url: str
            completed: bool
            encode_key: str
            encode_url: str
            index: float

        create_at: int
        encode_key: str
        encode_param: str
        encode_size: str
        encode_url: str
        key: str
        progress: List[Progress]
        script: str
        size: str
        status: str
        url: str

    data: Optional[Data] = None
    error: Optional[Error] = None
    success: bool


class OSSPresignedURLRequest(BaseModel):
    video_key: str


class OSSPresignedURLResponse(BaseModel):
    class Data(BaseModel):
        exist: bool
        url: str

    data: Optional[Data] = None
    error: Optional[Error] = None
    success: bool
