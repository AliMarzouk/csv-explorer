test_modules_names = ["lib.test.main_test"]


def run_tests():
    test_modules = map(__import__, test_modules_names)
    for test_module in test_modules:
        for i in dir(test_module):
            item = getattr(test_module, i)
            if callable(item):
                item()

if __name__ == '__main__':
    run_tests()