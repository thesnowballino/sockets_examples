import itertools
from time import time


def gen(s):
    for i in s:
        yield i

def gen_filename():
    pattern = "file-{}.jpeg"
    while True:
        t = int(time() * 1000)
        yield pattern.format(str(t))


if __name__ == "__main__":
    tasks = [gen("Eugene"), iter(range(6))]

    while tasks:
        task = tasks.pop(0)

        try:
            i = next(task)
            print(i)
            tasks.append(task)
        except StopIteration:
            pass
