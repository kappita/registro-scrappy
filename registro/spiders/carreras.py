import scrapy


class CarrerasSpider(scrapy.Spider):
    name = "carreras"
    allowed_domains = ["registro.usach.cl"]

    def start_requests(self):
        yield scrapy.Request("https://registro.usach.cl/index.php?ct=horario", self.parseFaculties)

    def parseFaculties(self, response):
        for option in response.xpath("/html/body/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/form/select/*")[1:]:
            yield scrapy.FormRequest(url="https://registro.usach.cl/index.php?ct=horario&mt=get_carreras", callback=self.parseCareers,
                             formdata={"idCombo1":f"{option.attrib['value']}"},
                             meta={"facultyId": option.attrib['value']})


    def parseCareers(self, response):
        facultyId = response.meta.get("facultyId")
        for option in response.xpath("/html/body/select/*")[1:]:
            yield {"facultyId": facultyId, "careerId": option.attrib['value'], "careerName": option.xpath("text()").get()}


