import asyncio
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel


# use str to store the path, because Path may not serializable on Windows
class TaskStatus(BaseModel):
    done: bool = False
    bt_downloaded_path: Optional[str] = None
    finalrip_downloaded_path: Optional[str] = None
    tg_uploaded: bool = False
    ex_status_dict: Optional[Dict[str, Any]] = None


class AsyncJsonStore:
    """
    a simple JSON store for task status.

    :param file_path: Path to the JSON file.
    """

    def __init__(self, file_path: Union[str, Path] = "store.json") -> None:
        self.file_path = Path(file_path)
        self.lock = asyncio.Lock()  # 使用 asyncio.Lock 确保线程安全
        self.data: Dict[str, TaskStatus] = self.load_data()

    def load_data(self) -> Dict[str, TaskStatus]:
        """
        Load data from the JSON file.
        """
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as file:
                try:
                    j = json.load(file)
                except json.JSONDecodeError:
                    return {}

                return {task_id: TaskStatus(**task) for task_id, task in j.items()}
        return {}

    async def save_data(self) -> None:
        """
        Save data to the JSON file.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            # convert TaskStatus objects to dictionaries
            data = {task_id: task.model_dump() for task_id, task in self.data.items()}
            json.dump(data, file, ensure_ascii=False, indent=4)

    async def check_task_exist(self, task_id: str) -> bool:
        """
        Check if a task exists.

        :param task_id: Task ID to check.
        """
        async with self.lock:
            return task_id in self.data

    async def add_task(self, task_id: str, status: TaskStatus) -> None:
        """
        Add a task to the store.

        :param task_id: Task ID to add.
        :param status: Task status.
        """
        async with self.lock:
            if task_id not in self.data:
                self.data[task_id] = status
                await self.save_data()
            else:
                raise KeyError(f"Task with ID '{task_id}' already exists.")

    async def get_task(self, task_id: str) -> TaskStatus:
        """
        Get a task by its ID.

        :param task_id: Task ID to get.
        """
        async with self.lock:
            if task_id in self.data:
                task = deepcopy(self.data.get(task_id))
                if task is None:
                    raise ValueError("Task value is None!")
                return task
            else:
                raise KeyError(f"Task with ID '{task_id}' not found.")

    async def update_task(self, task_id: str, status: TaskStatus) -> None:
        """
        Update a task's status and details.

        :param task_id: Task ID to update.
        :param status: New status.
        """
        async with self.lock:
            if task_id in self.data:
                self.data[task_id] = status
                await self.save_data()
            else:
                raise KeyError(f"Task with ID '{task_id}' not found.")

    async def delete_task(self, task_id: str) -> None:
        """
        Delete a task by its ID.

        :param task_id: Task ID to delete.
        """
        async with self.lock:
            if task_id in self.data:
                del self.data[task_id]
                await self.save_data()
            else:
                raise KeyError(f"Task with ID '{task_id}' not found.")
