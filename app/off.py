from urllib.parse import urljoin

from .i18n import translate as _
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
    html = []
    for tag in tags[0:3]:
        info = {
            "products": tag["products"],
            "name": tag["name"],
        }
        html.append(f'<li><a herf={tag["url"]}>')
        html.append(_("{products} products with {name}").format(**info))
        html.append("</a></li>")

    html = (
        [
            "<ul><p>",
            _("The total number of issues are {total_issues}").format(
                total_issues=total_issues
            ),
            "</p>",
        ]
        + html
        + ["</ul>"]
    )
    text = "".join(html)
    description = _("Data-quality issues related to")
    title = _("Data-quality issues")

    return text, source_url, description, title


def last_edit(url, query):
    """
    Helper function to return data for last-edits
    """
    search_url = f"{url}/api/v2/search"
    response_API = requests.get(search_url, params=query)
    data = response_API.json()
    counts = data["count"]
    tags = data["products"]

    html = []
    for tag in tags[0:10]:
        info = {
            "product_name": tag.get("product_name", ""),
            "code": tag["code"],
            "last_editor": tag.get("last_editor", ""),
            "edit_date": tag["last_edit_dates_tags"][0],
        }
        html.append("<li>")
        html.append(
            _("{product_name} ({code}) edited by {last_editor} on {edit_date}").format(
                **info
            )
        )
        html.append("</li>")
    html = (
        [
            "<ul><p>",
            _("Total number of edits {counts}").format(counts=counts),
            "</p>",
        ]
        + html
        + ["</ul>"]
    )
    text = "".join(html)
    description = _("last-edits issues related to")
    title = _("Last-edits")
    return text, description, title


def hungergame():
    """Helper function for making Translation easy"""
    description = _("Answer robotoff questions about")
    return description
