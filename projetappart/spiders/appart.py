# -*- coding: utf-8 -*-
import scrapy
import requests
import pandas as pd
from scrapy import Selector, Request

from projetappart.const import RechercheCategorie, Ville, TypeImmobilier, TypeBien, URL_LEBONCOIN, quartiers_toulon, \
    TypeLocation, TypeAnnonce
from projetappart.items import ProjetappartItem
from projetappart.utils.utils import parse_title, parse_prix, parse_relative_url, parse_pro, parse_type_bien, \
    parse_surface_bien, parse_installations, parse_description, parse_quartier


class AppartSpider(scrapy.Spider):
    name = 'appart'  # nom du spider
    allowed_domains = ['leboncoin.fr']
    start_urls = []
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

    # PARAMETRES DE RECHERCHE

    type_recherche = RechercheCategorie.LOCATIONS_IMMOBILIERES
    localisations = [Ville.TOULON]
    types_etat = [TypeImmobilier.NEUF, TypeImmobilier.ANCIEN]
    prix_min = 350   # exprimé en €
    prix_max = 650  # exprimé en €
    surface_min = 35  # exprimé en m2
    surface_max = None
    types_bien = [TypeBien.APPARTEMENT, TypeBien.MAISON]

    type_location = TypeLocation.NON_MEUBLEE  # None pour meublée et non-meublée
    type_annonce = TypeAnnonce.PARTICULIER  # None si indeterminé

    quartiers = quartiers_toulon  # None si non utilisé

    def start_requests(self):
        dict_params = {"category": str(self.type_recherche.value),
                       "locations": ','.join(map(lambda c: str(c.value), self.localisations)),
                       "price": str(self.prix_min) + '-' + str(self.prix_max),
                       "real_estate_type": ','.join(map(lambda c: str(c.value), self.types_bien))}

        if self.surface_min or self.surface_max:
            str_min = str(self.surface_min) if self.surface_min is not None else "min"
            str_max = str(self.surface_max) if self.surface_max is not None else "max"
            dict_params["square"] = str_min + '-' + str_max

        if self.type_annonce is not None:
            dict_params["owner_type"] = str(self.type_annonce.value)

        if self.type_recherche == RechercheCategorie.LOCATIONS_IMMOBILIERES and self.type_location is not None:
            dict_params["furnished"] = str(self.type_location.value)

        if self.type_recherche == RechercheCategorie.VENTES_IMMOBILIERES:
            dict_params["immo_sell_type"] = ','.join(map(lambda c: str(c.value), self.types_etat))

        return [scrapy.FormRequest(URL_LEBONCOIN,
                                   formdata=dict_params, method='GET')]

    def parse(self, response):

        # on va récupérer les wrappers
        wrappers_annonces = response.xpath('//li[@data-qa-id="aditem_container"]')

        for annonce in wrappers_annonces:
            relative_url = parse_relative_url(annonce)
            absolute_url = response.urljoin(relative_url)

            item = ProjetappartItem()
            title = parse_title(annonce)
            prix = parse_prix(annonce)
            pro = parse_pro(annonce)

            item['title'] = title
            item['prix'] = prix
            item['pro'] = pro
            item['url'] = absolute_url

            # on va scrapper l'annonce via la méthode parse_page
            yield Request(absolute_url, callback=self.parse_page, meta=item)

        relative_next_url = response.xpath('//ul[@class="_25feg"]/li[last()]/a/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        yield Request(absolute_next_url)

    def parse_page(self, response):
        type_bien = parse_type_bien(response)
        surface_bien = parse_surface_bien(response)
        description = parse_description(response)
        parse_installations(response, response.meta)
        parse_quartier(response, response.meta, self.quartiers)

        print(response.meta['terrasse'])

        response.meta['type_bien'] = type_bien
        response.meta['surface_m2'] = surface_bien
        response.meta['description'] = description

        yield response.meta




