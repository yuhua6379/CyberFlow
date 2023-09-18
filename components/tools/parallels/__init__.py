import concurrent.futures


def execute_tasks_in_parallel(func_list: list[callable], max_workers: int = 10):
    # 创建一个线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 使用线程池来执行任务，并获取Future对象
        futures = [executor.submit(func) for func in func_list]

        # 在主线程中等待结果
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        return results
