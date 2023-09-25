from typing import Any, Generator


def coroutine(generator_func):
    def inner(*args, **kwargs):
        g = generator_func(*args, **kwargs)
        # prime the coroutine
        g.send(None)
        return g
    # we can check by inspect.getgeneratorstate(coro)
    return inner


def subgen() -> Generator[None, Any, None]:
    message = yield
    print(f"Subgen recieved: {message}")


@coroutine
def average() -> Generator[float | None, float, None]:
    count: int = 0
    summ: float = 0
    avg: float | None = None
    while True:
        try:
            x: float = yield avg
        except StopIteration:
            # the loop is infinite, but we still can get StopIteration
            # by using .throw(exc) method.
            print("Done")
        else:
            count += 1
            summ += x
            avg = round(summ / count, 2)
