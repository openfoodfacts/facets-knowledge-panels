from collections import Counter
from enum import Enum
from typing import Literal, Optional, TypedDict

from fastapi import Query
from openfoodfacts import Country, Lang
from pydantic import BaseModel, Field, constr, validator


class HungerGameFilter(str, Enum):
    label = "label"
    category = "category"
    country = "country"
    brand = "brand"
    product_weight = "product_weight"

    @staticmethod
    def list():
        return [c.value for c in HungerGameFilter]


class Taxonomies(str, Enum):
    country = "country"
    nova_group = "nova_group"
    brand = "brand"
    category = "category"
    label = "label"
    packaging = "packaging"
    ingredient = "ingredient"
    additive = "additive"
    vitamin = "vitamin"
    mineral = "mineral"
    amino_acid = "amino_acid"
    nucleotide = "nucleotide"
    allergen = "allergen"
    state = "state"
    origin_of_ingredient = "origin"
    language = "language"
    other_nutritional_substances = "other_nutritional_substances"

    @staticmethod
    def list():
        return [c.value for c in Taxonomies]


FACET_TAG_QUERY = Query(
    title="Facet tag",
    description="Facet tag to use",
    examples=["category", "brand", "ingredient"],
)

VALUE_TAG_QUERY = Query(
    title="Value tag",
    description="Value tag to use",
    examples=["en:beers", "carrefour"],
)

SECONDARY_FACET_TAG_QUERY = Query(
    title="Secondary facet tag",
    description="Secondary facet tag, used on Open Food Facts website on nested facet pages "
    "(ex: /brand/[BRAND]/category/[CATEGORY]). It should be different than `facet_tag`",
    examples=["category", "brand", "ingredient"],
)

SECONDARY_VALUE_TAG_QUERY = Query(
    title="Secondary value tag",
    description="Secondary value tag, it should be different than `value_tag`",  # noqa: E501
    examples=["en:beers", "carrefour"],
)

LANGUAGE_CODE_QUERY = Query(
    title="language code 2-letter code",
    description="To return knowledge panels in native language",
)

COUNTRY_QUERY = Query(
    title="Country tag string",
    description="To return knowledge panels for specific country, ex: `france` or `fr`.",
)


# --------------------------------------------
# Response model class for the knowledge panels
# --------------------------------------------


class BaseTitleElement(BaseModel):
    """An element containing a title"""

    title: str = Field(
        description="title of the panel",
    )


class BaseTextElement(BaseModel):
    """An element with simple HTML to display"""

    html: Optional[str] = Field(
        default=None,
        description="Text to display in HTML format",
    )
    source_text: Optional[str] = Field(
        description="name of the source",
    )

    source_url: Optional[str] = Field(
        description="Link to the source",
    )


class BaseElement(BaseModel):
    """Element container"""

    element_type: str = Field(
        description="The type of the included element object."
        "The type also indicates which field contains the included element object. "
        """e.g. if the type is "text", the included element object will be in the "text_element" field.""",  # noqa: E501
    )
    text_element: BaseTextElement = Field(
        description="A text in simple HTML format to display.",
    )


class KnowledgePanelItem(BaseModel):
    """A Panel, made of multiple sub elements"""

    elements: Optional[list[BaseElement]] = None
    title_element: BaseTitleElement


class HungerGamePanel(TypedDict, total=False):
    """Panel linking to Hunger Games"""

    HungerGames: KnowledgePanelItem


class DataQualityPanel(TypedDict, total=False):
    """Panel with elements of data quality"""

    Quality: KnowledgePanelItem


class LastEditsPanel(TypedDict, total=False):
    """Panel reporting last edits for the facet"""

    LastEdits: KnowledgePanelItem


class WikidataPanel(TypedDict, total=False):
    """Panel with informations taken from wikidata"""

    WikiData: KnowledgePanelItem


class InformationPanel(TypedDict, total=False):
    """Panel with facet description."""

    Description: KnowledgePanelItem


class KnowledgePanel(
    HungerGamePanel, DataQualityPanel, LastEditsPanel, WikidataPanel, InformationPanel
):
    pass


class FacetResponse(BaseModel):
    # Return facetresponse l.e, all differnt knowledge panel
    knowledge_panels: KnowledgePanel | None = None


# Models related to information knowledge panel content


class KnowledgeContentItem(BaseModel):
    lang: Lang
    tag_type: Literal["label", "additive", "category"]
    value_tag: constr(min_length=3)
    content: constr(min_length=2)
    country: Country
    category_tag: str | None = None


class KnowledgeContent(BaseModel):
    items: list[KnowledgeContentItem]

    @validator("items")
    def unique_items(cls, v):
        count = Counter(
            (item.lang, item.tag_type, item.value_tag, item.country, item.category_tag)
            for item in v
        )
        most_common = count.most_common(1)
        if most_common and most_common[0][1] > 1:
            raise ValueError(f"more than 1 item with fields={most_common[0][0]}")
        return v
