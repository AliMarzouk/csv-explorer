import importlib

from .decorators import CUSTOM_DECORATOR_ATTR

test_modules_names = [".main_test"]

def run_tests():
    """Run all tests specified in the "test_modules_names" list.

    Goes through the modules specified in the "test_modules_names" list and executes all the 
    functions defined with the @custom_test decorator.
    you can use the command "python -m lib.test.test_runner" to run all the test defined.
    """
    test_modules = map(lambda name: importlib.import_module(name, "lib.test"), test_modules_names)
    for test_module in test_modules:
        for i in dir(test_module):
            item = getattr(test_module, i)
            if callable(item) and getattr(item, CUSTOM_DECORATOR_ATTR, False):
                item()

if __name__ == '__main__':
    run_tests()