from collections.abc import Callable
import functools
import traceback
# for reference: 
# see https://realpython.com/primer-on-python-decorators/#simple-decorators-in-python
# see https://www.artima.com/weblogs/viewpost.jsp?thread=240845#decorator-functions-with-decorator-arguments

CUSTOM_DECORATOR_ATTR = 'is_custom_test'

def custom_test(*test_inputs: list[tuple]):
    """Decorator to define a custom test.
    
    Executes the test function multiple times with the decorator's arguments as inputs and prints the result of the executions.
    The decorator takes a list of tuples in the format [(test_data, expected_result)].
    """
    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper():
            passed_tests = 0
            failed_tests = 0
            print(f"\n======= Executing {fn.__qualname__} ==============")
            for index, test_input in enumerate(test_inputs):
                try:
                    fn(test_input[0], test_input[1])
                    passed_tests += 1
                    print("|")
                    print(f"----> Run successfully ({index+1} / {len(test_inputs)})")
                except Exception as e:
                    failed_tests += 1
                    print("|")
                    print(f"----> Run failed ({index+1} / {len(test_inputs)}) - ", repr(e))
                    if type(e) != AssertionError:
                        traceback.print_exc()
            print("\n======= Execution end. Pass: {:.1f}% Failed: {:.1f}% ==============".format((passed_tests / (passed_tests + failed_tests))*100, (failed_tests / (passed_tests + failed_tests))*100))
        setattr(wrapper, CUSTOM_DECORATOR_ATTR, True)
        return wrapper
    return decorator