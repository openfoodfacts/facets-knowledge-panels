import urllib
from functools import cached_property

import wikidata.client


class WikiDataProperties:
    """some useful properties"""

    @cached_property
    def _client(self):
        return wikidata.client.Client()

    @cached_property
    def image_prop(self):
        return self._client.get("P18")

    @cached_property
    def OSM_prop(self):
        return self._client.get("P402")

    @cached_property
    def INAO_prop(self):
        return self._client.get("P3895")

    @cached_property
    def acceptable_daily_intake(self):
        return self._client.get("P2542")
        #estimate of the amount of a food additive, expressed on a body weight basis, that can be ingested daily over a lifetime without appreciable health risk

    @cached_property
    def Open_Food_Facts_food_additive_ID(self):
        return self._client.get("P1820")
        # Open Food Facts additive https://world.openfoodfacts.org/additives/

    @cached_property
    def E_number(self):
        return self._client.get("P628")
        #E number - for food additives - european system also used outside Europe.

    @cached_property
    def International_Numbering_System_number(self):
        return self._client.get("P4849")
        #International Numbering System number - for food additives - UN FAO identification system.

    @cached_property
    def JECFA_database_id(self):
        return self._client.get("P4852")
        #JECFA database ID - for food additives, pesticides and veterinary drugs present in foods - UN FAO database identifier.

    @cached_property
    def permitted_food_additive(self):
        return self._client.get("P4850")
        #permitted food additive - additives allowed to be present in a particular food product according to the UN FAO.

    @cached_property
    def maximum_food_additive_use_level(self):
        return self._client.get("P4851")
        # maximum food additive use level - used as a qualifier for permitted food additive (P4850) - maximum quantity of a food additive permitted to be present in a particular food product according to the UN FAO.

@cached_property
def gs1_country_code(self):
    return self._client.get("P3067")
    # GS1 Prefix - 3 digits at the start of a barcode, usually identifying the national GS1 Member Organization to which the manufacturer is registered (not necessarily where the product is actually made)

@cached_property
def gs1_company_prefix(self):
    return self._client.get("P3193")
    # company or organisation code, used in GS1 barcodes

@cached_property
def scoville_grade(self):
    return self._client.get("P2658")
    # for spices, peppers…

@cached_property
def unii(self):
    return self._client.get("P652")
    # UNII identifier - US unique identifier for ingredients.

@cached_property
def uk_national_fruit_collection_id(self):
    return self._client.get("P4288")

@cached_property
def findsmiley_id(self):
    return self._client.get("P3152")
    # identifier for Danish companies serving food

@cached_property
def alcohol_by_volume(self):
    return self._client.get("P2665")

@cached_property
def okp_id_of_the_good_or_service(self):
    return self._client.get("P3248")

@cached_property
def okpd_code_of_the_good_or_service(self):
    return self._client.get("P3245")

@cached_property
def okpd2_product_code(self):
    return self._client.get("P3250")

@cached_property
def usda_ndb_number(self):
    return self._client.get("P1978")

@cached_property
def ausnut_food_id(self):
    return self._client.get("P2759")

@cached_property
def nuttab_food_id(self):
    return self._client.get("P2760")

@cached_property
def fao_risk_status(self):
    return self._client.get("P2371")

@cached_property
def main_food_source(self):
    return self._client.get("P1034")

@cached_property
def image(self):
    return self._client.get("P18")

@cached_property
def shape(self):
    return self._client.get("P1419")

@cached_property
def product_certification(self):
    return self._client.get("P1389")

@cached_property
def made_from_material(self):
    return self._client.get("P186")

@cached_property
def country_of_origin(self):
    return self._client.get("P495")

@cached_property
def location_of_creation(self):
    return self._client.get("P1071")

@cached_property
def icd_code_to_food_allergies(self):
    return self._client.get("P493")
    # ICD-9 ID for food allergies

@cached_property
def plu_code(self):
    return self._client.get("P4030")

wikidata_props = WikiDataProperties()


def get_wikidata_entity(entity_id: str):
    client = wikidata.client.Client()
    return client.get(entity_id)


def image_thumbnail(image_url: str, width: int):
    """
    tries to build image thumbnail for wikimedia image
    """
    # only for pattern we know
    url = urllib.parse.urlparse(image_url)
    if url.path.startswith("/wikipedia/commons/"):
        # add components to get thumbnail
        dirs = url.path.split("/")
        dirs.insert(3, "thumb")
        dirs.append(f"{width}px-thumbnail.jpg")
        url = url._replace(path="/".join(dirs))
    return url.geturl()
