from collections.abc import Callable
import functools
# for reference: 
# see https://realpython.com/primer-on-python-decorators/#simple-decorators-in-python
# see https://www.artima.com/weblogs/viewpost.jsp?thread=240845#decorator-functions-with-decorator-arguments

def custom_test(*test_inputs: list[tuple]):
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper():
            print(f"\n======= Executing {fn.__qualname__} ==============")
            for index, test_input in enumerate(test_inputs):
                try:
                    fn(test_input[0], test_input[1])
                    print("|")
                    print(f"----> Run successfully ({index+1} / {len(test_inputs)})")
                except Exception as e:
                    print("|")
                    print(f"----> Run failed ({index+1} / {len(test_inputs)})")
                    print(e)
        return wrapper
    return decorator