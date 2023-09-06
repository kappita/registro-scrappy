import scrapy
import json


class RegistroSpider(scrapy.Spider):
    name = "registro"
    allowed_domains = ["registro.usach.cl"]
    start_urls = ["https://registro.usach.cl/index.php?ct=horario&mt=muestra_horario"]
    period = "2023-02"
    file = open("profesoresId.json", "r", encoding="utf-8")
    teachersIds = json.load(file)

    #data = []


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

            careerCode = tableData.xpath("./text()[2]").get()
            courseLevel = tableData.xpath("./text()[3]").get()

            if careerCode != None:
                careerCode = careerCode.strip()
            if courseLevel != None:
                courseLevel = courseLevel.strip()

            
            gettingTeachers = False
            for section in levelTable.xpath("./tr[3]/td[1]/table[1]/tr[2]/td[1]/font[1]/table[1]/*")[1:]:
                if len(section.xpath("./*")) == 9:
                    if gettingTeachers:
                        yield {"careerCode": careerCode,
                               "courseLevel": courseLevel,
                               "duration": dur,
                               "courseCode": courseCode,
                               "courseType": courseType,
                               "courseSection": courseSection,
                               "courseName": courseName,
                               "teachers": teachers}
                        
                    dur = section.xpath("./td[1]/strong/font/text()").get()
                    courseCode = section.xpath("./td[2]/strong/font/text()").get()
                    courseType = section.xpath("./td[3]/strong/font/text()").get()
                    courseSection = section.xpath("./td[4]/strong/font/text()").get()
                    courseName = section.xpath("./td[5]/strong/font/text()").get()
                    teacher = section.xpath("./td[8]/strong/font/text()").get()
                    schedule = section.xpath("./td[9]/strong/font/text()").getall()
                    if teacher != None and len(teacher.split(" ")) > 1 and not teacher.isspace():
                        teachers = [{"teacher": self.teachersIds[teacher],
                                        "schedule": schedule}]
                    else:
                        teachers = [{"teacher": None,
                                        "schedule": schedule}]
                        
                    gettingTeachers = False
                    yield {"careerCode": careerCode,
                           "courseLevel": courseLevel,
                           "duration": dur,
                           "courseCode": courseCode,
                           "courseType": courseType,
                           "courseSection": courseSection,
                           "courseName": courseName,
                           "teachers": teachers}

                elif len(section.xpath("./*")) == 7:
                    if gettingTeachers:
                        yield {"careerCode": careerCode,
                               "courseLevel": courseLevel,
                               "duration": dur,
                               "courseCode": courseCode,
                               "courseType": courseType,
                               "courseSection": courseSection,
                               "courseName": courseName,
                               "teachers": teachers}

                    dur = section.xpath("./td[1]/strong/font/text()").get()
                    courseCode = section.xpath("./td[2]/strong/font/text()").get()
                    courseType = section.xpath("./td[3]/strong/font/text()").get()
                    courseSection = section.xpath("./td[4]/strong/font/text()").get()
                    courseName = section.xpath("./td[5]/strong/font/text()").get()
                    teachers = []
                    gettingTeachers = True

                elif len(section.xpath("./*")) == 2:
                    teacher = section.xpath("./td[1]/strong/font/text()").get()
                    if teacher != None and len(teacher.split(" ")) > 1 and not teacher.isspace():
                        teachers.append({"teacher": self.teachersIds[teacher],
                                        "schedule": section.xpath("./td[2]/strong/font/text()").getall()})
                    else:
                        teachers.append({"teacher": None,
                                        "schedule": section.xpath("./td[2]/strong/font/text()").getall()})

            if gettingTeachers:
                yield {"careerCode": careerCode,
                       "courseLevel": courseLevel,
                       "duration": dur,
                       "courseCode": courseCode,
                       "courseType": courseType,
                       "courseSection": courseSection,
                       "courseName": courseName,
                       "teachers": teachers}
