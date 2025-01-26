import importlib


test_modules_names = [".main_test"]

def run_tests():
    test_modules = map(lambda name: importlib.import_module(name, "lib.test"), test_modules_names)
    for test_module in test_modules:
        for i in dir(test_module):
            item = getattr(test_module, i)
            if callable(item) and "test_" in i:
                item()

if __name__ == '__main__':
    run_tests()