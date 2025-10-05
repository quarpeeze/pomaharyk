import scrapy

class CourseSpider(scrapy.Spider):
    name = "course_spider"
    allowed_domains = ["is.muni.cz"]
    start_urls = [
        "https://is.muni.cz/predmet/phil/podzim2025/PLIN081"  
    ]

    def parse(self, response):
        # Try several ways to find the title
        title = (
            response.css("h2::text").get()
        )
        # we will also extract fields with teachers and other data about the subject. 
        # in the html it's a definition list with dt and dd tags
        fields = {}
        for dt, dd in zip(response.css("main#app_content dt"), response.css("main#app_content dd")):
            label = dt.xpath("normalize-space(string())").get()
            value = dd.xpath("normalize-space(string())").get()
            fields[label] = value

        if title:
            title = title.strip()
        else:
            self.logger.warning("smth went wrong:", response.url)

        yield {"url": response.url, "title": title, "content": fields}

