from urllib.parse import urljoin
import requests


def dataQuality(url, path):
    """
    Helper function to return issues for data-quality
    """
    source_url = urljoin(url, path)
    quality_url = f"{source_url}/data-quality.json"
    response_API = requests.get(quality_url)
    data = response_API.json()
    total_issues = data["count"]
    tags = data["tags"]
    html = "\n".join(
        f'<li><a href="{tag["url"]}">{tag["products"]} products with {tag["name"]}</a></li>'
        for tag in tags[0:3]
    )
    expected_html = f"<p>The total number of issues are {total_issues},here couples of issues</p><ul>{html}</ul>"

    return expected_html, source_url
