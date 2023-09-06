import json

file = open("profesores.json", "r", encoding="utf-8")
newFile = open("profesoresId.json", "w", encoding="utf-8")
teachers = json.load(file)

teacher_id = 0
indexedTeachers = {}
for entry in teachers:
    teacher = entry["teacher"]
    if teacher not in indexedTeachers:
        indexedTeachers[teacher] = teacher_id
        teacher_id += 1

text = json.dumps(indexedTeachers, ensure_ascii=False, indent=2)
newFile.write(text)
newFile.close()
file.close()

