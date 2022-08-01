from urllib.parse import urljoin
import requests


def data_quality(url, path):
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


def last_edit(url, query):
    """
    Helper function to return data for last-edits
    """
    search_url = f"{url}/api/v2/search"
    response_API = requests.get(search_url, params=query)
    data = response_API.json()
    counts = data["count"]
    tags = data["products"]

    html = "\n".join(
        f'<li>{tag["product_name"]} ({tag["code"]}) edited by {tag["last_editor"]} on {tag["last_edit_dates_tags"][0]}</li>'
        for tag in tags[0:10]
        if "product_name" in tag
    )

    html = f"<ul><p>Total number of edits {counts} </p>\n {html}</ul>"

    return html


def wikidata(query, value):
    url = "https://world.openfoodfacts.org/api/v2/taxonomy"
    response_API = requests.get(url, params=query)
    data = response_API.json()
    tag = data[value]
    if "wikidata" in tag:
        entity = tag["wikidata"]["en"]
    return entity
