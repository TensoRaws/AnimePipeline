from animepipeline.store.task import AsyncJsonStore, TaskStatus


async def test_task_store() -> None:
    store = AsyncJsonStore()

    # 添加一个任务
    await store.add_task("task_1", TaskStatus())

    # 获取任务
    task = await store.get_task("task_1")
    print(task)

    # 更新任务状态
    await store.update_task("task_1", task)
    print(await store.get_task("task_1"))

    # 删除任务
    await store.delete_task("task_1")
