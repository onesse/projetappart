# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy import Selector, Request

from projetappart.items import ProjetappartItem
from projetappart.utils.utils import parse_title, parse_prix, parse_relative_url, parse_pro, parse_type_bien, \
    parse_surface_bien, parse_bonus, parse_description


class AppartSpider(scrapy.Spider):
    name = 'appart'  # nom du spider
    allowed_domains = ['leboncoin.fr']
    start_urls = ['https://www.leboncoin.fr/recherche/?category=9&locations=La Garde_83130&&immo_sell_type=old,new&price=50000-225000&real_estate_type=1,2']
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"

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
        parse_bonus(response, response.meta)

        response.meta['type_bien'] = type_bien
        response.meta['surface_m2'] = surface_bien
        response.meta['description'] = description

        yield response.meta




