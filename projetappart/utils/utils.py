import re

from scrapy import Selector

from projetappart.const import list_bonus
from projetappart.items import ProjetappartItem


def parse_title(selector: Selector):
    """
    Extrait le titre d'une annonce
    :param selector:
    :return: string
    """
    title = selector.xpath('.//a/@title').extract_first()
    title = re.sub('[^A-Za-z0-9éèà&² ]+', '', title)
    return title


def parse_prix(selector: Selector):
    """
    Extrait le prix d'une annonce
    :param selector:
    :return: int
    """
    prix_str = selector.xpath('.//span[@itemprop="priceCurrency"][@content="EUR"]/text()').extract_first()
    prix_str = prix_str.replace(" ", "")
    return int(prix_str)


def parse_pro(selector: Selector):
    """
    Extrait le type de l'annonce
    :param selector:
    :return: boolean
    """
    description = selector.xpath('.//p[@itemprop="alternateName"]/span/text()').extract_first()

    return 'Pro' in description if description is not None else False


def parse_relative_url(selector: Selector):
    """
    Extrait l'url relative
    :param selector:
    :return: string
    """
    return selector.xpath('.//a[@class="clearfix trackable"]/@href').extract_first()


def parse_type_bien(selector: Selector):
    """
    Extrait le type de bien
    :param selector:
    :return: string
    """
    return selector.xpath('//div[@data-qa-id="criteria_item_real_estate_type"]/div/div[last()]/text()').extract_first()


def parse_surface_bien(selector: Selector):
    """
    Extrait la surface du bien en m²
    :param selector:
    :return: string
    """
    suface_str = selector.xpath('//div[@data-qa-id="criteria_item_square"]/div/div[last()]/text()').extract_first()
    surface = re.findall(r'\d+', suface_str)
    return surface[0] if len(surface) > 0 else None


def parse_description(selector: Selector):
    """
    Extrait la desciption du bien
    :param selector:
    :return: string
    """
    description = selector.xpath('//div[@data-qa-id="adview_description_container"]/div/span/text()').extract()
    description = ''.join(description)
    description = re.sub('[^A-Za-z0-9éèà&² ]+', '', description)
    return description


def parse_bonus(selector: Selector, item: ProjetappartItem):
    """
    Extrait la surface du bien en m²
    :param selector:
    :return: string
    """
    description = parse_description(selector)

    if description is not None:
        description = description.lower()

    for key, key_words in list_bonus.items():
        if description is not None:
            for key_word in key_words:
                if key_word in description.lower():
                    item[key] = True
                else:
                    item[key] = False
        else:
            item[key] = False
    return item
