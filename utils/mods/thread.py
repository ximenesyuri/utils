import threading
from typed import Str, Function, Maybe, Dict, Tuple, Int, Any, List
from concurrent.futures import ThreadPoolExecutor, Future

class thread:
    def __init__(self, workers: Maybe(Int)=None):
        if workers is not None and workers < 1:
            workers = 1
        self._executor = ThreadPoolExecutor(max_workers=workers)
        self._futures: Dict[str, Future] = {}
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

    def get(self, name: Str) -> Any:
        with self._lock:
            future = self._futures.get(name)
        if future is None:
            raise KeyError(f"No task found with name '{name}'.")
        return future.result()

    def list(self) -> List(Str):
        with self._lock:
            return list(self._futures.keys())
