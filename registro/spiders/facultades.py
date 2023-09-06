import scrapy


class FacultadesSpider(scrapy.Spider):
    name = "facultades"
    allowed_domains = ["registro.usach.cl"]

    def start_requests(self):
        yield scrapy.Request("https://registro.usach.cl/index.php?ct=horario", self.parseFaculties)

    def parseFaculties(self, response):
        for option in response.xpath("/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/select/*")[1:-1]:
            yield {"facultyId": option.attrib['value'], "facultyName": option.xpath("text()").get()[2:]}
