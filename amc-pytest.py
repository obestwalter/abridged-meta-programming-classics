"""Code from the slides for pico-pytest."""
import sys
from itertools import chain
from pathlib import Path

import pytest


def get_module(path):
    path = Path(path)
    sys.path.insert(0, str(path.parent))
    name = path.stem
    module = __import__(name)
    print(f"<get_module('{path}') => import '{name}'>", file=sys.stderr)
    return module


def collect_test_functions(module):
    return [
        obj
        for obj in module.__dict__.values()
        if obj.__class__.__name__ == "function" and obj.__name__.startswith("test_")
    ]


name2fixture = {}


def fixture(function):
    name2fixture[function.__name__] = function
    print(f"<fixture({function.__name__}) => registered>", file=sys.stderr)


def execute_test(function):
    names = function.__code__.co_varnames[:function.__code__.co_argcount]
    kwargs = {name: f() for name, f in name2fixture.items() if name in names}
    result = "."
    try:
        function(**kwargs)  # pass as keyword arguments => order doesn't matter
        return "passed"
    except Exception as e:
        result = "F"
        return e
    finally:
        print(result, end="")


def mark_attacher_factory(name):
    def attach_mark(function):
        print(
            f"<attach_mark({function.__name__}) => '{name}'>", file=sys.stderr
        )
        try:
            function.pico_pytest_marks.append(name)
        except AttributeError:
            function.pico_pytest_marks = [name]
        return function
    return attach_mark


class MarkAttacherFactoryFactory:
    def __getattr__(self, name):  # called when attribute lookup fails
        return mark_attacher_factory(name)


def satisfies_expression(expression, markers):
    newTokens = []
    for token in expression.split():
        if token in markers:
            newTokens.append("True")
        elif token in ["and", "or", "not"]:
            newTokens.append(token)
        else:
            newTokens.append("False")
    return eval(" ".join(newTokens))


def filter_tests(tests, expression):
    remaining = []
    for test in tests:
        markers = getattr(test, "pico_pytest_marks", [])
        if satisfies_expression(expression, markers):
            remaining.append(test)
    if deselected := len(tests) - len(remaining):  # 3.8 assignment expression
        print(
            f"<filter_tests(...)> => deselected {deselected} tests>",
            file=sys.stderr
        )
    return remaining


def display_collected(tests):
    print(f"collected {len(tests)} tests:")
    for test in tests:
        print(f"\t<{type(test).__name__} {test.__name__}>")


def report(results):
    failed = {
        test: result for test, result in results.items()
        if not isinstance(result, str)
    }
    if failed:
        print("\n\nFAILURES:")
        for test, e in failed.items():
            result = f"{e.__class__.__name__}('{e.args[0]}')"
            print(f"{test.__name__}: {result}")
        print(f"\nexecuted: {len(results)}, failed: {len(failed)}")
    else:
        print(f"\nexecuted: {len(results)} (all is fine!)")


def pico_pytest(path=Path.cwd(), collect_only=False, mark_expression=""):
    paths = list(Path(path).glob("**/test_*.py"))
    modules = [get_module(path) for path in paths]
    tests = list(chain(*[collect_test_functions(m) for m in modules]))
    if mark_expression:
        tests = filter_tests(tests, mark_expression)
    if collect_only:
        display_collected(tests)
    else:
        report({test: execute_test(test) for test in tests})


if __name__ == '__main__':
    pytest.fixture = fixture
    pytest.mark = MarkAttacherFactoryFactory()
    pico_pytest()
    print()
    pico_pytest(collect_only=True)
    print()
    pico_pytest(collect_only=True, mark_expression="charlie or lucy")
