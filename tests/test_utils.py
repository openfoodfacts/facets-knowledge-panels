class MockResponse:
    def __init__(self, json_content):
        self.json_content = json_content

    def json(self):
        return self.json_content


def mock_get_factory(target_url, json_content):
    """generate a mock to patch request.get with a json response"""

    def mock_get(url, **kwargs):
        assert url == target_url
        assert kwargs == {
            "fields": "product_name,code,last_editor,last_edit_dates_tags",
            "sort_by": "last_modified_t",
            "labels_tags_en": "vegan",
        }
        return MockResponse(json_content)

    return mock_get
