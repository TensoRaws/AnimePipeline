import asyncio

import pytest

from animepipeline.pool.task import AsyncTaskExecutor


async def example_task(task_id: str, duration: int) -> None:
    # Example task function
    print(f"Task {task_id} started, will take {duration} seconds.")
    await asyncio.sleep(duration)
    print(f"Task {task_id} completed.")


@pytest.mark.asyncio
async def test_task_executor() -> None:
    executor = AsyncTaskExecutor()

    for task_id in range(114):
        await executor.submit_task(f"task{task_id}", example_task, f"task{task_id}", 3)
        print(f"Task {task_id} has been submitted.")

    await executor.wait_all_tasks()

    assert len(executor.tasks) == 114
    for task_id in range(114):
        assert await executor.task_status(f"task{task_id}") == "Completed"


@pytest.mark.asyncio
async def test_task_executor_shutdown() -> None:
    executor = AsyncTaskExecutor()

    for task_id in range(114):
        await executor.submit_task(f"task{task_id}", example_task, f"task{task_id}", 300)
        print(f"Task {task_id} has been submitted.")

    await executor.shutdown()

    print(executor.tasks)

    assert len(executor.tasks) == 114
    for task_id in range(114):
        assert await executor.task_status(f"task{task_id}") == "Pending"


@pytest.mark.asyncio
async def test_task_dump() -> None:
    executor = AsyncTaskExecutor()

    await executor.submit_task(f"task{1}", example_task, f"task{1}", 0)
    await asyncio.sleep(1)
    await executor.submit_task(f"task{1}", example_task, f"task{1}", 0)
