# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from projetappart.const import a_rejeter


class ProjetappartPipeline(object):
    def process_item(self, item, spider):
        # Rejet des maisons/apparts en viager
        if any(rejet in item.get('title').lower() or rejet in item.get('description').lower() for rejet in a_rejeter):
            print(f"item {item.get('title')} contient un mot interdit")
            return None

        return item
