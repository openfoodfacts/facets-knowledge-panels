import requests


def lastEdit(url, query):
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
    )

    html = f"<ul><p>Total number of edits {counts} </p>\n {html}</ul>"

    return html
