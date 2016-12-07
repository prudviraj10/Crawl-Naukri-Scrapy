import scrapy
from scrapy.http import Request
from Naukri.items import Job_Categories_Item
from Naukri.items import Job_Item
import logging
logging.basicConfig()

class Job_Categories_Naukri_Spider(scrapy.Spider):
    name = 'NC'
    allowed_domains = ['naukri.com']
    start_urls = ['https://www.naukri.com/jobs-by-category']
    
    def __init__(self):
        logger = logging.getLogger('customlog')

    def parse(self,response):
        # self.logger.info('Parse function called on %s', response.url)
        for j in response.xpath('//div[@class="lmrWrap wrap"]/div/div/div/a'):
            item = Job_Categories_Item()
            title = j.xpath('text()').extract()
            url = j.xpath('@href').extract()
            if title != [] and url != []:
                item['link'] = url[0]
                item['title'] = title[0]
                count = 0
                yield Request(url[0], callback=self.parse_jobs,meta={'jobCategory':title[0],'count':count,'parentLink':url[0]})
                yield item

    def parse_jobs(self,response):
        try:
            jobc = response.meta['jobCategory']
            parentLink = response.meta['parentLink']
            count = response.meta['count']+1
            for j in response.xpath('//div[@itemtype="http://schema.org/JobPosting"]'):
                item = Job_Item()
                item['jobCategory'] = jobc
                item['depth'] = count
                item['jobCategoryLink'] = parentLink
                item['link'] = j.xpath('a/@href').extract()
                item['title'] = j.xpath('a/span[@itemprop="hiringOrganization"]/text()').extract()
                item['experienceRequirements'] = j.xpath('a/span[@itemprop="experienceRequirements"]/text()').extract()
                item['jobLocation'] = j.xpath('a/span/span[@itemprop="jobLocation"]/text()').extract()
                item['skills'] = j.xpath('a/div/div/span[@itemprop="skills"]/text()').extract()
                item['JobDescription'] = j.xpath('a/div/span[@itemprop="description"]/text()').extract()
                item['baseSalary'] = j.xpath('div/span[@itemprop="baseSalary"]/text()').extract()
                item['jobPoster'] = j.xpath('div/div/a/text()').extract()
                item['date'] = j.xpath('div/div/span[@class="date"]/text()').extract()
                item['jobType'] = j.xpath('span/@class').extract()[1]
                yield item
            next_page = response.xpath('//div[@class="pagination"]/a/@href').extract()
            if next_page != []:
                ind = response.xpath('//div[@class="pagination"]/a/button/text()').extract().index(u'Next')
                yield scrapy.Request(response.urljoin(next_page[ind]), callback=self.parse_jobs \
                 ,meta={'jobCategory':jobc,'count':count,'parentLink':parentLink})
        except exception as e:
            print e
