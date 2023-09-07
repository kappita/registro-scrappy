import scrapy


class ProfesoresSpider(scrapy.Spider):
    name = "profesores"
    allowed_domains = ["registro.usach.cl"]
    period = "2023-02"
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
            yield scrapy.FormRequest(url="https://registro.usach.cl/index.php?ct=horario&mt=muestra_horario",
                                     callback=self.parseTeachers,
                                     formdata={"id_facultad": facultyId,
                                       "id_list_carrera": option.attrib['value'],
                                       "id_periodo": self.period,
                                       "enterButton": "Elegir"})

    def parseTeachers(self, response):
        table = response.xpath("/html/body/center/table[1]")
        for levelTable in table.xpath("/html/body/center//table"):            
            for section in levelTable.xpath("./tr[3]/td[1]/table[1]/tr[2]/td[1]/font[1]/table[1]/*")[1:]:
                if len(section.xpath("./*")) == 9:
                    teacher = section.xpath("./td[8]/strong/font/text()").get()
                    if teacher != None and not teacher.isspace() and len(teacher.split(" ")) > 1:
                        yield {"teacher": section.xpath("./td[8]/strong/font/text()").get().strip()}

                elif len(section.xpath("./*")) == 2:
                    teacher = section.xpath("./td[1]/strong/font/text()").get()
                    if teacher != None and not teacher.isspace() and len(teacher.split(" ")) > 1:
                        yield {"teacher": section.xpath("./td[1]/strong/font/text()").get().strip()}
                    



