import pytest

from src.utils import pascal_to_snake_case


@pytest.mark.parametrize(
    "name, expected",
    [
        ("PascalCase", "pascal_case"),
        ("CamelCaseExample", "camel_case_example"),
        ("AnotherExampleHere", "another_example_here"),
        ("SimpleTest", "simple_test"),
        ("Test", "test"),
        ("A", "a"),
        ("", ""),
        ("a", "a"),
    ],
)
def test_pascal_to_snake_case(name, expected):
    assert pascal_to_snake_case(name) == expected
