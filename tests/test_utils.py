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


class DictAttr(dict):
    """dict where you can also access values as attributes"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


def mock_wikidata_get(expected_entity, values):
    """Generate a mock to patch wikidata.Client.get with a fake response object

    param str expected_entity: the entity that you want to test is used
    """

    def mock_get(client, entity, *args, **kwargs):
        assert entity == expected_entity
        return DictAttr(values)

    return mock_get


def tidy_html(html):
    """
    Helper function that return pretiffy html
    """
    html = BeautifulSoup(html, "html.parser").prettify()
    return html.strip()
