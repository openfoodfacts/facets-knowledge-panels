from bs4 import BeautifulSoup


class MockResponse:
    def __init__(self, json_content):
        self.json_content = json_content

    def json(self):
        return self.json_content


def mock_get_factory(target_url, expected_kwargs={}, json_content=None):
    """generate a mock to patch request.get with a json response"""

    def mock_get(url, **kwargs):
        assert url == target_url
        assert kwargs == expected_kwargs
        return MockResponse(json_content)

    return mock_get


def tidy_html(html):
    """
    Helper function that return pretiffy html
    """
    html = BeautifulSoup(html, "html.parser").prettify()
    return html.strip()
