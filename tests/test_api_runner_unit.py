import unittest

from src.api_runner import APIRunner


class FakeResponse:
    def __init__(self, lines):
        self._lines = lines

    def iter_lines(self):
        for line in self._lines:
            yield line


class APIRunnerUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = APIRunner(token="dummy", tenant_id="dummy")

    def test_extract_sql_from_uppercase_sql_marker(self):
        text = 'SQL: SELECT id, name FROM users WHERE status = "active"'
        extracted = self.runner._extract_sql_from_string(text)
        self.assertEqual(extracted, 'SELECT id, name FROM users WHERE status = "active"')

    def test_parse_sse_stream_can_find_sql_in_nested_text_field(self):
        response = FakeResponse(
            [
                b'data: {"data": {"message": "thinking..."}}',
                b'data: {"data": {"message": "SQL: SELECT count(*) FROM orders"}}',
                b'data: [DONE]',
            ]
        )

        sql = self.runner._parse_sse_stream(response, row_index=1)

        self.assertEqual(sql, "SELECT count(*) FROM orders")


if __name__ == "__main__":
    unittest.main()
