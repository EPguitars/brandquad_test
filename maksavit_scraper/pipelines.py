# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import json

from itemadapter import ItemAdapter


class MaksavitScraperPipeline:
    def open_spider(self, spider):
        self.file = open(f"example.json", 'w', encoding="UTF=8")
        self.file.write('[\n')

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False, indent=4) + ",\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.seek(self.file.tell() - 3, os.SEEK_SET)
        self.file.truncate()
        self.file.write('\n]')
        self.file.close()
