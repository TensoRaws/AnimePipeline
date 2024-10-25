import asyncio
from typing import Any, Callable, Dict


class AsyncTaskExecutor:
    """
    A simple async task executor that can submit tasks and check their status.
    This class uses asyncio to run tasks concurrently.
    """

    def __init__(self) -> None:
        self.lock = asyncio.Lock()
        self.tasks: Dict[str, asyncio.Task] = {}

    async def submit_task(self, task_id: str, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """
        Submit a task to the executor.

        :param task_id: The task ID.
        :param func: The function to run asynchronously.
        :param args: The arguments to pass to the function.
        :param kwargs: The keyword arguments to pass to the function.
        """
        async with self.lock:
            if task_id in self.tasks:
                return  # Task is already running

            # Wrap the function in asyncio.create_task to run it concurrently
            self.tasks[task_id] = asyncio.create_task(func(*args, **kwargs))

    async def task_status(self, task_id: str) -> str:
        """
        Check the status of a task.

        :param task_id: The task ID to check.
        """
        async with self.lock:
            if task_id in self.tasks and not self.tasks[task_id].done():
                return "Pending"
            elif task_id in self.tasks and self.tasks[task_id].done():
                return "Completed"
            else:
                return "Unknown"

    async def shutdown(self) -> None:
        """
        Cancel all running tasks and shutdown the executor.
        """
        async with self.lock:
            for task in self.tasks.values():
                if not task.done():
                    task.cancel()

    async def wait_all_tasks(self) -> None:
        """
        Wait for all tasks to complete.
        """
        async with self.lock:
            await asyncio.gather(*self.tasks.values())
