# API Reference

Knowledge panel facets is a simple api that allow user to get knowledge-panels based on the different facets

The api must be prefixed with this `/knowledge_panel?`.
The full url look like 
`http://127.0.0.1:8000/knowledge_panel?facet_tag={desired-facet}&value_tag={facet-value}&lang_code={language}&country={desired-country}`

## Knowledge Panels

### Get knowledge-panels [GET]

- Parameters:

  - facet_tag (str) - Take a facet like (`label`,`category`,`brands` etc) you can see more available facet [here](https://world.openfoodfacts.org/) in Explore poducts by.
  - value_tag (str, optional) - filter by value tag, i.e fetching facet_tag based on this value (ex : `en:beers`,`fr:fitou`)
  - lang_code (str, optional) - To get translated data (defualt lang: `en`)
  - country (str, optional) - Return knowledge-panels from a specific country (ex: `france`)
  
- Response 200 (application/json)

#### Example

Feteched knowledge-panels based on these parameters
Full url `http://127.0.0.1:8000/knowledge_panel?facet_tag=category&value_tag=fr:fitou&country=france`

- Parameters:

  - facet_tag (str) - `category`
  - value_tag (str, optional) - `fr:fitou`
  - country (str, optional) -  `france`
  
- Response 200 (application/json)

```json
{
  "knowledge_panels": [
    {
      "hunger-game": {
        "elements": [
          {
            "element_type": "text",
            "text_element": {
              "html": "<p><a href='https://hunger.openfoodfacts.org/questions?country=france&type=category&value_tag=fr%3Afitou'>Answer robotoff questions about fr:fitou category</a></p>\n"
            }
          }
        ]
      }
    },
    {
      "Quality": {
        "title": "Data-quality issues",
        "subtitle": "Data-quality issues related to france category fr:fitou",
        "source_url": "https://fr-en.openfoodfacts.org/category/fr:fitou/data-quality",
        "elements": [
          {
            "element_type": "text",
            "text_element": "<ul><p>The total number of issues are 16</p><li><a herf=https://fr-en.openfoodfacts.org/category/fr:fitou/data-quality/alcoholic-beverages-category-without-alcohol-value>29 products with alcoholic-beverages-category-without-alcohol-value</a></li><li><a herf=https://fr-en.openfoodfacts.org/category/fr:fitou/data-quality/ecoscore-production-system-no-label>27 products with ecoscore-production-system-no-label</a></li><li><a herf=https://fr-en.openfoodfacts.org/category/fr:fitou/data-quality/ecoscore-threatened-species-ingredients-missing>23 products with ecoscore-threatened-species-ingredients-missing</a></li></ul>"
          }
        ]
      }
    },
    {
      "LastEdits": {
        "title": "Last-edits",
        "subtitle": "last-edits issues related to france category fr:fitou",
        "source_url": "https://fr-en.openfoodfacts.org/category/fr:fitou?sort_by=last_modified_t",
        "elements": [
          {
            "element_type": "text",
            "text_element": "<ul><p>Total number of edits 29</p><li>Fitou Rouge (3245414134980) edited by chevalstar on 2022-08-04</li><li>Fitou (3331560501001) edited by teolemon on 2022-07-05</li><li>Fitou (3331560500332) edited by teolemon on 2022-07-05</li><li>Fitou (3331560500059) edited by packbot on 2022-02-11</li><li>Fitou (3222471837832) edited by packbot on 2022-02-11</li><li>Fitou 2011 (3288841016658) edited by packbot on 2022-02-11</li><li>Domaine du Tauch - Fitou (3288841031811) edited by packbot on 2022-02-11</li><li>Réserve des Tamaris 2010 - Fitou (3660989136663) edited by packbot on 2022-02-11</li><li>FITOU (3021891807131) edited by packbot on 2022-02-11</li><li>Fitou 2014 (3186127765149) edited by packbot on 2022-02-11</li></ul>"
          }
        ]
      }
    },
    {
      "WikiData": {
        "title": "wiki-data",
        "subtitle": "French wine appellation",
        "source_url": "https://www.wikidata.org/wiki/Q470974",
        "elements": [
          {
            "element_type": "text",
            "text_element": "Fitou AOC",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Paziols_%28France%29_Vue_du_village.jpg"
          },
          {
            "element_type": "links",
            "wikipedia": "https://en.wikipedia.org/wiki/Fitou_AOC",
            "open_street_map": "https://www.openstreetmap.org/relation/2727716",
            "INAO": "https://www.inao.gouv.fr/produit/6159"
          }
        ]
      }
    }
  ]
}
```