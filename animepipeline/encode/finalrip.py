import asyncio
import gc
import mimetypes
import time
from pathlib import Path
from typing import Optional, Union

import httpx
from httpx import AsyncClient
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_random

from animepipeline.config import FinalRipConfig
from animepipeline.encode.type import (
    GetTaskProgressRequest,
    GetTaskProgressResponse,
    NewTaskRequest,
    NewTaskResponse,
    OSSPresignedURLRequest,
    OSSPresignedURLResponse,
    PingResponse,
    RetryMergeRequest,
    RetryMergeResponse,
    StartTaskRequest,
    StartTaskResponse,
    TaskNotCompletedError,
)
from animepipeline.util.video import VIDEO_EXTENSIONS


class FinalRipClient:
    def __init__(self, config: FinalRipConfig):
        self.client = AsyncClient(base_url=str(config.url), headers={"token": str(config.token)}, timeout=30)

    async def ping(self) -> PingResponse:
        try:
            response = await self.client.get("/")
            return PingResponse(**response.json())
        except Exception as e:
            logger.error(f"Error ping: {e}")
            raise e

    async def _new_task(self, data: NewTaskRequest) -> NewTaskResponse:
        try:
            response = await self.client.post("/api/v1/task/new", params=data.model_dump())
            return NewTaskResponse(**response.json())
        except Exception as e:
            logger.error(f"Error creating task: {e}, {data}")
            raise e

    async def _start_task(self, data: StartTaskRequest) -> StartTaskResponse:
        try:
            response = await self.client.post("/api/v1/task/start", params=data.model_dump())
            return StartTaskResponse(**response.json())
        except Exception as e:
            logger.error(f"Error starting task: {e}, {data}")
            raise e

    async def _get_task_progress(self, data: GetTaskProgressRequest) -> GetTaskProgressResponse:
        try:
            response = await self.client.get("/api/v1/task/progress", params=data.model_dump())
            return GetTaskProgressResponse(**response.json())
        except Exception as e:
            raise e

    async def _get_oss_presigned_url(self, data: OSSPresignedURLRequest) -> OSSPresignedURLResponse:
        try:
            response = await self.client.get("/api/v1/task/oss/presigned", params=data.model_dump())
            return OSSPresignedURLResponse(**response.json())
        except Exception as e:
            logger.error(f"Error getting presigned URL: {e}, {data}")
            raise e

    async def _retry_merge(self, data: RetryMergeRequest) -> RetryMergeResponse:
        try:
            response = await self.client.post("/api/v1/task/retry/merge", params=data.model_dump())
            return RetryMergeResponse(**response.json())
        except Exception as e:
            logger.error(f"Error retrying merge: {e}, {data}")
            raise e

    async def check_task_exist(self, video_key: str) -> bool:
        try:
            get_task_progress_response = await self._get_task_progress(GetTaskProgressRequest(video_key=video_key))
            return get_task_progress_response.success
        except Exception:
            return False

    async def check_task_completed(self, video_key: str) -> bool:
        try:
            get_task_progress_response = await self._get_task_progress(GetTaskProgressRequest(video_key=video_key))
            if not get_task_progress_response.success:
                logger.error(f"Error getting task progress: {get_task_progress_response.error.message}")  # type: ignore
                return False
            return get_task_progress_response.data.encode_url != ""  # type: ignore
        except Exception as e:
            logger.error(f"Error checking task completed: {e}, video_key: {video_key}")
            return False

    async def check_task_all_clips_done(self, video_key: str) -> bool:
        try:
            get_task_progress_response = await self._get_task_progress(GetTaskProgressRequest(video_key=video_key))
            if not get_task_progress_response.success:
                logger.error(f"Error getting task progress: {get_task_progress_response.error.message}")  # type: ignore
                return False

            for clip in get_task_progress_response.data.progress:  # type: ignore
                if not clip.completed:
                    return False

            return True
        except Exception as e:
            logger.error(f"Error checking task all clips done: {e}, video_key: {video_key}")
            return False

    async def retry_merge(self, video_key: str) -> None:
        retry_merge_response = await self._retry_merge(RetryMergeRequest(video_key=video_key))
        if not retry_merge_response.success:
            logger.error(f"Error retrying merge: {retry_merge_response.error.message}")  # type: ignore

    @retry(wait=wait_random(min=3, max=5), stop=stop_after_attempt(5))
    async def upload_and_new_task(self, video_path: Union[str, Path]) -> None:
        """
        use file name as video_key, gen oss presigned url, upload file, and new_task, all in one function

        :param video_path: local video file path
        """
        if not Path(video_path).exists():
            logger.error(f"File not found: {video_path}")
            raise FileNotFoundError(f"File not found: {video_path}")

        if Path(video_path).suffix not in VIDEO_EXTENSIONS:
            logger.error(f"Only support these video extensions: {', '.join(VIDEO_EXTENSIONS)}")
            raise ValueError("Only support these video extensions: " + ", ".join(VIDEO_EXTENSIONS))

        # gen oss presigned url
        video_key = Path(video_path).name
        try:
            oss_presigned_url_response = await self._get_oss_presigned_url(OSSPresignedURLRequest(video_key=video_key))
            if not oss_presigned_url_response.success:
                logger.error(f"Error getting presigned URL: {oss_presigned_url_response.error.message}")  # type: ignore
                raise ValueError(f"Error getting presigned URL: {oss_presigned_url_response.error.message}")  # type: ignore
        except Exception as e:
            logger.error(f"Error getting presigned URL: {e}")
            raise e

        if not oss_presigned_url_response.data.exist:  # type: ignore
            try:
                content_type = mimetypes.guess_type(video_path)[0]
            except Exception:
                content_type = "application/octet-stream"

            # upload file
            try:
                logger.info(f"Uploading file: {video_path}")
                t0 = time.time()

                # 这里不要用异步，会内存泄漏
                def _upload_file() -> None:
                    with open(video_path, mode="rb") as v:
                        video_content = v.read()
                        logger.info(f"Read file Successfully! path: {video_path} time: {time.time() - t0:.2f}s")
                        response = httpx.put(
                            url=oss_presigned_url_response.data.url,  # type: ignore
                            content=video_content,
                            headers={"Content-Type": content_type},
                            timeout=60 * 60,
                        )
                        if response.status_code != 200:
                            raise IOError(f"Error uploading file: {response.text}")

                _upload_file()
                del _upload_file
                gc.collect()
                logger.info(f"Upload file Successfully! path: {video_path} time: {time.time() - t0:.2f}s")
            except Exception as e:
                logger.error(f"Error in uploading file: {video_path}: {e}")
                raise e

            await asyncio.sleep(2)

        # new task
        new_task_response = await self._new_task(NewTaskRequest(video_key=video_key))
        if not new_task_response.success:
            logger.error(f"Error creating task: {new_task_response.error.message}")  # type: ignore

    async def start_task(
        self, video_key: str, encode_param: str, script: str, slice: Optional[bool] = True, timeout: Optional[int] = 20
    ) -> None:
        """
        start encode task

        :param video_key: video_key of the task
        :param encode_param: encode param
        :param script: encode script
        :param slice: cut video into clips or not
        :param timeout: clip timeout, default 20 minutes
        """
        resp = await self._start_task(
            StartTaskRequest(
                video_key=video_key, encode_param=encode_param, script=script, slice=slice, timeout=timeout
            )
        )
        if not resp.success:
            logger.warning(f"Failed to start finalrip task: {resp.error.message}")  # type: ignore

    async def download_completed_task(self, video_key: str, save_path: Union[str, Path]) -> None:
        """
        download completed task to local

        :param video_key: video_key of the task
        :param save_path: local save path
        """
        if not await self.check_task_completed(video_key):
            raise TaskNotCompletedError()

        get_task_progress_response = await self._get_task_progress(GetTaskProgressRequest(video_key=video_key))

        try:
            logger.info(f"Downloading completed task: {save_path} ...")
            t0 = time.time()

            def _download_file() -> None:
                with open(save_path, mode="wb") as v:
                    response = httpx.get(
                        url=get_task_progress_response.data.encode_url,  # type: ignore
                        timeout=60 * 60,
                    )
                    if response.status_code != 200:
                        raise IOError(f"Error downloading file: {response.text}")
                    v.write(response.content)

            _download_file()
            del _download_file
            gc.collect()
            logger.info(f"Download completed task Successfully! path: {save_path}, time: {time.time() - t0:.2f}s")
        except Exception as e:
            logger.error(f"Error in downloading completed task: {save_path}: {e}")
            raise e
