# API Reference

Knowledge panel facets is a simple api that allow user to get knowledge-panels based on the different facets

The api must be prefixed with this `/knowledge_panel?`.
The full url look like 
`http://127.0.0.1:8000/knowledge_panel?facet_tag={desired-facet}&value_tag={facet-value}&lang_code={language}&country={desired-country}`

- API Documentation with interactive "try-out": http://127.0.0.1:8000/docs

## Knowledge Panels

### Get knowledge-panels [GET]

- Parameters:

  - facet_tag (str) - Take a facet like (`label`,`category`,`brands` etc) you can see more available facet [here](https://world.openfoodfacts.org/) in Explore poducts by.
  - value_tag (str, optional) - filter by value tag, i.e fetching facet_tag based on this value (ex : `en:beers`,`fr:fitou`)
  - lang_code (str, optional) - To get translated data (defualt lang: `en`)
  - country (str, optional) - Return knowledge-panels from a specific country (ex: `france`)
  
- Response 200 (application/json)