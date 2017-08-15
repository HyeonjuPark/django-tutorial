# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from django.db.utils import IntegrityError
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime
from scrapy.selector import Selector

class DjangoWriterPipeline(object):

    def process_item(self, item, spider):
      if spider.conf['DO_ACTION']: #Necessary since DDS v.0.9+
            try:
                print('HJ start saving')
                item['post_site'] = spider.ref_object

                checker_rt = SchedulerRuntime(runtime_type='C')
                checker_rt.save()
                item['checker_runtime'] = checker_rt

                print(item['foo'])

                if len(item['foo']) != 0:
                    selector = Selector(text=item['foo'])
                    options = selector.xpath('//option')
                    option_items = []
                    for option in options:
                        option_items.append(option.xpath("text()").extract())
                    print(option_items)
                    option_items.pop(0)
                    item['foo'] = option_items
                    # item['foo'] = json.dumps(option_items)

                print(item['foo'])
                item.save()
                spider.action_successful = True
                dds_id_str = str(item._dds_item_page) + '-' + str(item._dds_item_id)
                spider.struct_log("{cs}Item {id} saved to Django DB.{ce}".format(
                    id=dds_id_str,
                    cs=spider.bcolors['OK'],
                    ce=spider.bcolors['ENDC']))

            except IntegrityError as e:
                print('HJ integrity error')
                spider.log(str(e), logging.ERROR)
                spider.log(str(item._errors), logging.ERROR)
                raise DropItem("Missing attribute.")
      else:
          print('HJ not do_action')
          if not item.is_valid():
              spider.log(str(item._errors), logging.ERROR)
              raise DropItem("Missing attribute.")

      return item

class ScraperPipeline(object):
    def process_item(self, item, spider):
        return item
