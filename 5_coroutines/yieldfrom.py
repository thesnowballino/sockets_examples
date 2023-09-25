from typing import Any, Generator


class MyException(Exception):
    pass


def subgen() -> Generator[None, Any, str]:
    while True:
        try:
            message = yield
        except StopIteration:
            break
        except MyException:
            print("My exception!")
            break
        else:
            print(f"Message: {message}")

    return "Return from subgen()"


def delegating_generator() -> Generator[None, Any, None]:
    # Basically the code below emulates `yield from` construction (without `return` and more exception handling).
    # The main point of `yield from` is that we can communicate with the subgenerator directly
    # bypassing the delegating generator.

    # sg = subgen()
    # next(sg)  # prime coro
    # while True:
    #     try:
    #         data = yield
    #         sg.send(data)  # send received data to subgenerator immediately.
    #     except StopIteration as exc:
    #         sg.throw(exc)  # throw received data to subgenerator immediately.
    #     except Exception as exc:
    #         print("Some other exception...")
    #         sg.throw(exc)

    result = yield from subgen()
    print(result)
