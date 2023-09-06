import scrapy


class RamosSpider(scrapy.Spider):
    name = "ramos"
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
                                     callback=self.parseCourses,
                                     formdata={"id_facultad": facultyId,
                                       "id_list_carrera": option.attrib['value'],
                                       "id_periodo": self.period,
                                       "enterButton": "Elegir"})

    def parseCourses(self, response):
        table = response.xpath("/html/body/center/table[1]")

        # Sections where there's one professor or none and its info is inside the <tr>
        # This can be due to the section having a determinated schedule, but not a designated teacher
        # Sections where there's one or more professors outside the <tr>, having dedicated <tr>s.
        for levelTable in table.xpath("/html/body/center//table"):
            tableData = levelTable.xpath("./tr[1]/td[1]/table[1]/tr[2]/td[3]")
            dur = None
            courseId = None
            courseName = None
            level = tableData.xpath("./text()[3]").get()
            careerCode = tableData.xpath("./text()[2]").get()
            for section in levelTable.xpath("./tr[3]/td[1]/table[1]/tr[2]/td[1]/font[1]/table[1]/*")[1:]:
                if len(section.xpath("./*")) in [7, 9]:
                    if section.xpath("./td[2]/strong/font/text()").get() != courseId:
                        dur = section.xpath("./td[1]/strong/font/text()").get()
                        courseId = section.xpath("./td[2]/strong/font/text()").get()
                        courseName = section.xpath("./td[5]/strong/font/text()").get()
                        yield {"careerId": careerCode,"courseId": courseId, "courseName": courseName, "dur": dur, "level": level}




