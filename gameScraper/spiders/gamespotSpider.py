# -*- coding: utf-8 -*-
import scrapy


class GamespotspiderSpider(scrapy.Spider):
    name = "gamespotSpider"
    allowed_domains = ["gamespot.com"]
    start_urls = (
        'http://www.gamespot.com/reviews/',
    )

    def parse(self, response):

        print("DUDEE")
        print(response)
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
        for k in genre_mapping:
            print(k)

    def parseJo(self, response):
        genres = response.xpath('//*[@id="review_filter_type_genre"]/option')
        genre_mapping = {}
        for i in genres:
            extracted_number = i.xpath('.//@value').extract()[0]
            extracted_genre = i.xpath('.//text()').extract()[0]
            try:
                number = int(extracted_number)
                genre_mapping[number] = extracted_genre
            except ValueError:
                pass

        print(genre_mapping)


        for i in genre_mapping:
            print(i)
            headers = {}
            headers['review_filter_type[platform]'] = 'all'
            headers['review_filter_type[genre]'] = i[0]

            print(i)
            yield scrapy.Request(url='http://www.gamespot.com/reviews/', headers=headers, meta={"genre_id": i[0], "genre_title": i[1]}, callback=self.parse_review_page)


    def parse_review_page(self, response):
        pass


#         go to next page using page header

