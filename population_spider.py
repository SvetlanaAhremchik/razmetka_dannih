    # start_urls = ["https://worldometers.info"]

import scrapy


class PopulationSpider(scrapy.Spider):
    name = 'population_spider'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        # Извлечение данных из таблицы
        for row in response.css('table#example2 tbody tr'):
            yield {
                'Country': row.css('td:nth-child(2) a::text').get(),
                'Population': row.css('td:nth-child(3)::text').get(),
                'Area (km²)': row.css('td:nth-child(4)::text').get(),
                'Density (per km²)': row.css('td:nth-child(5)::text').get(),
                'Growth Rate (%)': row.css('td:nth-child(6)::text').get(),
                'World Share (%)': row.css('td:nth-child(7)::text').get(),
            }

        # Переход на следующую страницу, если она существует
        next_page = response.css('a[title="Go to next page"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
            pass