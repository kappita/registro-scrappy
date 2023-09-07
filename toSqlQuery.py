import json

def bruh(x):
  return f'({x["facultyId"]}, "{x["facultyName"][3:]}")'

def bruh2(x):
  return f'{x["careerId"]}, "{x["careerName"].split(" ")[2]}", {x["facultyId"]}'

def join(x):
  text = x[0]
  for i in x[1:]:
      text += "," + i
  return text

def bruh3(x):
  bruh =  []
  for key, value in x.items():
    bruh.append({"teacherId": value, "teacherName": key})
  return bruh

def bruh4(x):
  return f'({x["teacherId"]}, "{x["teacherName"]}")'

def bruh5(x):
  return f'({x["courseId"]}, "{x["courseName"]}", "{x["dur"]}")'

def bruh6(x):
  return f'({x["careerId"]}, {x["courseId"]}, {x["level"]})'

def bruh7(x):
  return f'("{x["sectionId"]}", {x["courseId"]}, {x["courseSection"]}, "{x["courseType"]}", {x["sectionQuota"]}, {x["sectionSignedUp"]}, "{x["period"]}")'

def bruh8(x):
  return f'("{x["sectionId"]}", {x["careerId"]})'

def bruh9(x, sectionId, teacher):
  return f'("{sectionId}", {teacher}, {x["weekday"]}, {x["block"]}, "{x["classroom"]}")'

# FIX
def bruh10(x):
  values = []
  for teacher in x["teachers"]:
    for block in teacher["schedule"]:
      values.append(bruh9(block, x["sectionId"], teacher["teacher"]))
  return values

  


file = open("registro/spiders/profesoresId.json", "r", encoding="utf8")
teacherIds = json.load(file)
file.close()

file = open("facultades.json", "r", encoding="utf8")
faculties:list = json.load(file)
file.close()

file = open("carreras.json", "r", encoding="utf8")
careers = json.load(file)
file.close()

file = open("ramos.json", "r", encoding="utf8")
courses = json.load(file)
file.close()

file = open("profesores.json", "r", encoding="utf8")
teachers = json.load(file)
file.close()

file = open("registro.json", "r", encoding="utf8")
registry = json.load(file)
file.close()

file = open("bruh.txt", "w", encoding="utf8")
query = ""

query += f'INSERT OR IGNORE INTO faculties (id, name) VALUES {join(list(map(bruh, faculties)))};\n'

query += f'INSERT OR IGNORE INTO careers (id, name, faculty_id) VALUES {join(list(map(bruh2, careers)))};\n'

query += f'INSERT OR IGNORE INTO teachers (name) VALUES {join(list(map(bruh4, bruh3(teacherIds))))};\n'

query += f'INSERT OR IGNORE INTO courses (id, name, course_duration) VALUES {join(list(map(bruh5, courses)))};\n'
query += f'INSERT OR IGNORE INTO coursesCareers (career_id, course_id, course_level) VALUES {join(list(map(bruh6, courses)))};\n'

query += f'INSERT OR REPLACE INTO sections (section_id, course_id, code, course_type, quota, signed_up, period) VALUES {join(list(map(bruh7, registry)))};\n'
query += f'INSERT OR REPLACE INTO sectionscareers (section_id, career_id) VALUES {join(list(map(bruh8, registry)))};\n'
for section in registry:
  query += f'INSERT OR REPLACE INTO schedules (section_id, teacher_id, weekday, block, classroom) VALUES {join(bruh10(section))};\n'



file.write(query)

