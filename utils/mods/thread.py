import threading
from typed import Str, Function, Maybe, Dict, Tuple, Int, Any, List
from concurrent.futures import ThreadPoolExecutor

class thread:
    def __init__(self, workers: Maybe(Int)=None):
        if workers is not None and workers < 1:
            workers = 1
        self._executor = ThreadPoolExecutor(max_workers=workers)
        self._futures = {}
        self._lock = threading.Lock()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._executor.shutdown(wait=True)

    def __iter__(self):
        with self._lock:
            return iter(self._futures.keys())

    def new(self, name: Str, task: Function, *args: Tuple, **kwargs: Dict) -> None:
        with self._lock:
            if name in self._futures:
                raise ValueError(f"Task with name '{name}' already exists.")
            future = self._executor.submit(task, *args, **kwargs)
            self._futures[name] = future

    def restart(self, name: Str, task: Function, *args: Tuple, **kwargs: Dict) -> None:
        """
        Restart a task at the same position in the internal order:
        - The key `name` must already exist.
        - Its current Future must be done().
        - A new Future is submitted and stored under the same key.
        """
        with self._lock:
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
        """
        Remove a task from this thread. If it is still running, attempt to cancel it.
        """
        with self._lock:
            future = self._futures.pop(name, None)
        if future is None:
            raise KeyError(f"No task found with name '{name}'.")
        if not future.done():
            future.cancel()

    def get(self, name: Str) -> Any:
        with self._lock:
            future = self._futures.get(name)
        if future is None:
            raise KeyError(f"No task found with name '{name}'.")
        return future.result()

    def list(self) -> List(Str):
        with self._lock:
            return list(self._futures.keys())

