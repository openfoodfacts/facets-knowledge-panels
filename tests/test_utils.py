class MockResponse:
    def __init__(self, json_content):
        self.json_content = json_content

    def json(self):
        return self.json_content


def mock_get_factory(target_url, json_content):
    """generate a mock to patch request.get with a json response"""

    def mock_get(url):
        assert url == target_url
        return MockResponse(json_content)

    return mock_get
