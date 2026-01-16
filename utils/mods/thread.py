from typed import Str, Function, Maybe, Dict, Tuple, Int, Any, List
from concurrent.futures import ThreadPoolExecutor

class thread:
    def __init__(self, workers: Maybe(Int) = None):
        if workers is not None and workers < 1:
            workers = 1
        self._executor = ThreadPoolExecutor(max_workers=workers)
        self._futures = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._executor.shutdown(wait=True)

    def __iter__(self):
        return iter(self._futures.keys())

    def new(self, name: Str, task: Function, *args: Tuple, **kwargs: Dict) -> None:
        if name in self._futures:
            raise ValueError(f"Task with name '{name}' already exists.")
        future = self._executor.submit(task, *args, **kwargs)
        self._futures[name] = future

    def restart(self, name: Str, task: Function, *args: Tuple, **kwargs: Dict) -> None:
        future = self._futures.get(name)
        if future is None:
            raise KeyError(f"No task found with name '{name}'.")
        if not future.done():
            raise RuntimeError(
                f"Cannot restart task '{name}': task is still running."
            )
        new_future = self._executor.submit(task, *args, **kwargs)
        self._futures[name] = new_future

    def rm(self, name: Str) -> None:
        future = self._futures.pop(name, None)
        if future is None:
            raise KeyError(f"No task found with name '{name}'.")
        if not future.done():
            future.cancel()

    def get(self, name: Str) -> Any:
        future = self._futures.get(name)
        if future is None:
            raise KeyError(f"No task found with name '{name}'.")
        return future.result()

    def list(self) -> List(Str):
        return list(self._futures.keys())

    def exists(self, name: Str) -> bool:
        return name in self._futures

    def done(self, name: Str) -> bool:
        future = self._futures.get(name)
        if future is None:
            raise KeyError(f"No task found with name '{name}'.")
        return future.done()

    def running(self, name: Str) -> bool:
        return not self.done(name)
