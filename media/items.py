from scrapy.item import Item, Field


class Item(Item):
    id = Field()
    text = Field()
    label = Field()