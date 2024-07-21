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
    def inao_product_id(self):
        return self._client.get("P3895")
        # INAO product ID

    @cached_property
    def ratebeer_brewery_id(self):
        return self._client.get("P2905")
        # RateBeer brewery ID

    @cached_property
    def acceptable_daily_intake(self):
        return self._client.get("P2542")
        # estimate of the amount of a food additive, expressed on a body weight basis, that can be ingested daily over a lifetime without appreciable health risk

    @cached_property
    def Open_Food_Facts_food_additive_ID(self):
        return self._client.get("P1820")
        # Open Food Facts additive https://world.openfoodfacts.org/additives/

    @cached_property
    def open_food_facts_food_category_id(self):
        return self._client.get("P1821")
        # Open Food Facts food category ID

    @cached_property
    def E_number(self):
        return self._client.get("P628")
        # E number - for food additives - european system also used outside Europe.

    @cached_property
    def International_Numbering_System_number(self):
        return self._client.get("P4849")
        # International Numbering System number - for food additives - UN FAO identification system.

    @cached_property
    def JECFA_database_id(self):
        return self._client.get("P4852")
        # JECFA database ID - for food additives, pesticides and veterinary drugs present in foods - UN FAO database identifier.

    @cached_property
    def permitted_food_additive(self):
        return self._client.get("P4850")
        # permitted food additive - additives allowed to be present in a particular food product according to the UN FAO.

    @cached_property
    def maximum_food_additive_use_level(self):
        return self._client.get("P4851")
        # maximum food additive use level - used as a qualifier for permitted food additive (P4850) - 
        # maximum quantity of a food additive permitted to be present in a particular food product according to the UN FAO.

    @cached_property
    def gs1_country_code(self):
        return self._client.get("P3067")
        # GS1 Prefix - 3 digits at the start of a barcode, usually identifying the national GS1 Member Organization to which the manufacturer is registered 
        #(not necessarily where the product is actually made)

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
        # alcohol by volume

    @cached_property
    def jmpr_database_id(self):
        return self._client.get("P4853")
        # JMPR database ID

    @cached_property
    def beer_bitterness(self):
        return self._client.get("P6088")
        # beer bitterness

    @cached_property
    def beer_color(self):
        return self._client.get("P6089")
        # beer color

    @cached_property
    def foodon_id(self):
        return self._client.get("P6767")
        # FoodOn ID

    @cached_property
    def fema_number(self):
        return self._client.get("P8266")
        # FEMA number

    @cached_property
    def food_energy(self):
        return self._client.get("P7971")
        # food energy

    @cached_property
    def tasteatlas_id(self):
        return self._client.get("P5456")
        # TasteAtlas ID

    @cached_property
    def course(self):
        return self._client.get("P8431")
        # course

    @cached_property
    def drizly_product_id(self):
        return self._client.get("P8858")
        # Drizly product ID

    @cached_property
    def barnivore_product_id(self):
        return self._client.get("P9031")
        # Barnivore product ID

    @cached_property
    def thecocktaildb_drink_id(self):
        return self._client.get("P9056")
        # TheCocktailDB drink ID

    @cached_property
    def thecocktaildb_ingredient_id(self):
        return self._client.get("P9057")
        # TheCocktailDB ingredient ID

    @cached_property
    def fl_number(self):
        return self._client.get("P9066")
        # FL number

    @cached_property
    def open_food_facts_ingredient_id(self):
        return self._client.get("P5930")
        # Open Food Facts ingredient ID

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
        # USDA NDB number

    @cached_property
    def ausnut_food_id(self):
        return self._client.get("P2759")

    @cached_property
    def nuttab_food_id(self):
        return self._client.get("P2760")

    @cached_property
    def vivc_grape_variety_id(self):
        return self._client.get("P3904")
        # VIVC grape variety ID

    @cached_property
    def foodex2_code(self):
        return self._client.get("P4637")
        # FoodEx2 code

    @cached_property
    def gems_code(self):
        return self._client.get("P4695")
        # GEMS Code

    @cached_property
    def ciqual2017_id(self):
        return self._client.get("P4696")
        # CIQUAL2017 ID

    @cached_property
    def inran_italian_food_id(self):
        return self._client.get("P4729")
        # INRAN Italian Food ID

    @cached_property
    def fao_risk_status(self):
        return self._client.get("P2371")
        # FAO risk status

    @cached_property
    def main_food_source(self):
        return self._client.get("P1034")
        # main food source

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

    @cached_property
    def edibility(self):
        return self._client.get("P789")
        # edibility

    @cached_property
    def foods_traditionally_associated(self):
        return self._client.get("P868")
        # foods traditionally associated

    @cached_property
    def marmiton_id(self):
        return self._client.get("P9769")
        # Marmiton ID

    @cached_property
    def food_com_id(self):
        return self._client.get("P9840")
        # Food.com ID

    @cached_property
    def eambrosia_id(self):
        return self._client.get("P9854")
        # eAmbrosia ID

    @cached_property
    def swedish_food_agency_food_id(self):
        return self._client.get("P9894")
        # Swedish Food Agency food ID

    @cached_property
    def bbc_food_id(self):
        return self._client.get("P9925")
        # BBC Food ID

    @cached_property
    def lambic_info_id(self):
        return self._client.get("P10172")
        # Lambic.Info ID

    @cached_property
    def faoterm_id(self):
        return self._client.get("P10584")
        # FAOTERM ID

    @cached_property
    def culinary_heritage_of_switzerland_id(self):
        return self._client.get("P11217")
        # Culinary Heritage of Switzerland ID

    @cached_property
    def dizionario_dei_prodotti_dop_e_igp_id(self):
        return self._client.get("P11773")
        # Dizionario dei prodotti DOP e IGP ID

    @cached_property
    def qualigeo_id(self):
        return self._client.get("P11794")
        # Qualigeo ID


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
