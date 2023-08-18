from pathlib import Path

import markdown
import yaml
from openfoodfacts.types import Country, Lang

from app.models import KnowledgeContent, KnowledgeContentItem


def find_kp_html_path(
    root_dir: Path, tag_type: str, value_tag: str, country: Country, lang: Lang
) -> Path | None:
    """Return the Path of the HTML page related to an information knowledge panel, if it exists.

    We first check that a knowledge panel exists for the provided `country`, with a fallback
    to `Country.world` otherwise.

    Args:
        root_dir: the root directory where HTML pages are located
        tag_type: the tag type (ex: 'category', 'label',...)
        value_tag: the tag value (ex: `en:ab-agriculture-biologique`)
        country: the Country of the information knowledge panel
        lang: the language code of the information knowledge panel

    Returns:
        Path: the Path of the HTML page or None if not found
    """
    base_dir = root_dir / tag_type / value_tag.replace(":", "_")
    if not base_dir.exists():
        return None

    html_file_paths = list(base_dir.glob("*.html"))
    # file names follows the schema '{country}_{lang}.html'
    # Filter by lang
    html_file_paths = [p for p in html_file_paths if lang.value == p.stem.split("_")[1]]

    if not html_file_paths:
        return None

    country_targets = [country] if country is Country.world else [country, Country.world]
    for country_target in country_targets:
        country_specific_html_files = [
            p for p in html_file_paths if country_target.value == p.stem.split("_")[0]
        ]

        if country_specific_html_files:
            return country_specific_html_files[0]

    return None


def generate_file_path(root_dir: Path, item: KnowledgeContentItem) -> Path:
    """Generate a file path unique to the knowledge content item.

    The generated path depends on the `tag_type`, the `value_tag`, the
    `country` and `lang`.

    Args:
        root_dir: the root directory where HTML pages are located
        item: the knowledge content item

    Returns:
        Path: the path where the HTML page should be saved
    """
    return (
        root_dir
        / item.tag_type
        / item.value_tag.replace(":", "_")
        / f"{item.country.name}_{item.lang.name}.html"
    )


def build_content(root_dir: Path, file_path: Path):
    """Build content as HTML pages from `file_path` (a YAML file).

    The YAML file should follows the schema of `KnowledgeContent`.
    Files are saved as HTML files under `root_dir`, see
    `generate_file_path` for more information about how paths
    are generated.

    Args:
        root_dir: the root directory where HTML pages are located
        file_path: the input YAML file path
    """
    with file_path.open("r") as f:
        data = yaml.safe_load(f)
    knowledge_items = KnowledgeContent.parse_obj(data)

    for item in knowledge_items.items:
        output_path = generate_file_path(root_dir, item)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown.markdown(item.content))
