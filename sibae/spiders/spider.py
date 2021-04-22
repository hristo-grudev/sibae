import scrapy

from scrapy.loader import ItemLoader

from ..items import SibaeItem
from itemloaders.processors import TakeFirst


class SibaeSpider(scrapy.Spider):
	name = 'sibae'
	start_urls = ['https://www.sib.ae/press-centre']

	def parse(self, response):
		post_links = response.xpath('//a[@title="See Details"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="event-box press_detailbox"]//text()[normalize-space() and not(ancestor::h2 | ancestor::a | ancestor::div[@class="date-position"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="date-position"][not(@style)]//text()[normalize-space()]').getall()
		date = [p.strip() for p in date if '{' not in p]
		date = ' '.join(date).strip()

		item = ItemLoader(item=SibaeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
