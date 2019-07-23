import pytest
from slate_utils.docs.utils import pkv_to_dict


def test_pkv_to_dict():
    xml = """
        <p>
            <k>key1</k>
            <v>value1</v>
        </p>
        <p>
            <k>key2</k>
            <v>value2</v>
        </p>
        <p>
            <k>key2</k>
            <v>value2.1</v>
        </p>"""
    expected = {'key1': 'value1',
                'key2': ['value2', 'value2.1']}
    assert pkv_to_dict(xml) == expected
