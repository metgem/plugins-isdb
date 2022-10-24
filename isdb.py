"""MetGem plugin to download ISDB"""

__version__ = '1.2'
__description__ = "MetGem plugin to download ISDB"
__author__ = "Nicolas Elie"
__email__ = "nicolas.elie@cnrs.fr"
__copyright__ = "Copyright 2019-2022, CNRS/ICSN"
__license__ = "GPLv3"

import json


# noinspection PyUnresolvedReferences
class ISDB(DbSource):

    name = "ISDB"
    page = "https://doi.org/10.5281/zenodo.5607185"
    items_base_url = ""

    def get_items(self, tree):
        json_s = tree.find('.//script[@type="application/ld+json"]').text
        json_load = json.loads(json_s)
        description = json_load.get('description',
                                    '\u003cp\u003eAn In Silico spectral DataBase (\u003cstrong\u003eISDB\u003c/strong\u003e) of natural products calculated\u0026nbsp;from structures aggregated in the frame of the LOTUS Initiative.\u003c/p\u003e\n\n\u003cp\u003eThis spectral file is in positive ionisation mode only. Fragmented using cfm-predict 3.0\u0026nbsp;\u003ca href=\"https://cfmid.wishartlab.com/\"\u003ehttps://cfmid.wishartlab.com/\u003c/a\u003e\u003c/p\u003e\n\n\u003cp\u003eIntensities at the low, medium and high energy level have been meaned.\u003c/p\u003e\n\n\u003cp\u003e\u0026nbsp;\u003c/p\u003e\n\n\u003cp\u003eIn silico spectral database preparation and use for dereplication initially\u0026nbsp;described in\u0026nbsp;\u003cem\u003eIntegration of Molecular Networking and In-Silico MS/MS Fragmentation for Natural Products Dereplication\u003c/em\u003e \u003ca href=\"https://doi.org/10.1021/ACS.ANALCHEM.5B04804\"\u003ehttps://doi.org/10.1021/ACS.ANALCHEM.5B04804\u003c/a\u003e\u003c/p\u003e\n\n\u003cp\u003eSee \u003ca href=\"http://oolonek.github.io/ISDB/\"\u003ehttp://oolonek.github.io/ISDB/\u003c/a\u003e for associated spectral matching scripts\u003c/p\u003e\n\n\u003cp\u003eLOTUS Initiative initially described in\u0026nbsp;\u003ca href=\"https://doi.org/10.7554/eLife.70780\"\u003ehttps://doi.org/10.7554/eLife.70780\u003c/a\u003e\u003c/p\u003e\n\n\u003cp\u003e\u0026nbsp;\u003c/p\u003e\n\n\u003cp\u003e\u0026nbsp;\u003c/p\u003e')
        identifier = json_load.get('identifier', '')
        version = json_load.get('version', '')
        version = f"Version {version}" if version else ''
        date = json_load.get('datePublished', '')
        if identifier:
            description = f"<a href='{identifier}'>{identifier}</a>\n{description}"
        if date:
            description = f"({date}) {description}"
        if version:
            description = f"{version} {description}"

        hrefs = []

        for distrib in json_load.get('distribution', []):
            if distrib.get('@type', '') == 'DataDownload':
                href = distrib['contentUrl']
                if href:
                    hrefs.append(href)
        if hrefs:
            yield "In-Silico Database", hrefs, description
