# -*- coding: utf-8 -*-
import scrapy


class GamespotspiderSpider(scrapy.Spider):
    name = "gamespotSpider"
    allowed_domains = ["gamespot.com"]
    start_urls = (
        'http://www.gamespot.com/reviews/',
    )

    def build_headers(self, genre_id, platform='all'):
        headers = {}
        headers['review_filter_type[platform]'] = platform
        headers['review_filter_type[genre]'] = genre_id
        return headers

    def parse(self, response):
        # get available genres
        genres = response.xpath('//*[@id="review_filter_type_genre"]/option')
        genre_mapping = []
        for i in genres:
            extracted_number = i.xpath('.//@value').extract()[0]
            extracted_genre = i.xpath('.//text()').extract()[0]

            print(extracted_genre)
            try:
                number = int(extracted_number)
                genre_mapping.append((number, extracted_genre,))
            except ValueError:
                pass

        print(genre_mapping)

        for i in genre_mapping:
            headers = {}
            headers['review_filter_type[platform]'] = 'all'
            headers['review_filter_type[genre]'] = i[0]

            print(i)
            # For every genre start the crawler for the pages in this genre
            # yield ipv return
            yield scrapy.Request(url='http://www.gamespot.com/reviews/', headers=headers,
                                 meta={"genre_id": i[0], "genre_title": i[1]}, callback=self.start_review_pages_crawl)

    # This method starts the crawling for all the review pages in the genre
    def start_review_pages_crawl(self, response):
        last_page = response.xpath('//*[@id="js-sort-filter-results"]/ul/li[last()]/a/@href').extract()[0].split('=')[
                    -1:][0]
        print('last page ', last_page)
        for i in range(0, int(last_page)):
            header = self.build_headers(response.meta['genre_id'])
            header['page'] = str(i)
            req = scrapy.Request(url='http://www.gamespot.com/reviews/', headers=header,
                                 callback=self.parse_review_page, meta=response.meta)
            yield req

    def parse_review_page(self, response):
        print('parsing review')
        reviews_xpath = response.xpath('//*[@id="js-sort-filter-results"]/section/article')

        genre = response.meta['genre_title']
        for i in reviews_xpath:
            review = {}
            review['review_url'] = 'http://www.gamespot.com' + i.xpath('.//a/@href').extract()[0]
            review['rating'] = i.xpath('.//a/div[1]/div/strong/text()').extract()[0]
            review['title'] = i.xpath('.//a/div[2]/h3/text()').extract()[0]

            # get platforms
            platforms_xpath = i.xpath('.//a/div[2]/div/ul/li')
            # unique platforms , so use a set

            platforms = []
            # the first i is not a platform
            for i in platforms_xpath[1:]:
                p = i.xpath('.//text()').extract()[0]
                if p not in platforms:
                    platforms.append(p)

            review['platforms'] = platforms
            review['genre'] = genre

            yield review

# go to next page using page header
