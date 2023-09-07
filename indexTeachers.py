import json

file = open("profesores.json", "r", encoding="utf-8")
teachers = json.load(file)
file.close()

try:
    oldIds = open("registro/spiders/profesoresId.json", "r", encoding="utf-8")
    ids = json.load(oldIds)
    oldIds.close()
except:
    ids = {}

teacher_id = len(ids)
for entry in teachers:
    teacher = entry["teacher"]
    if teacher not in ids:
        ids[teacher] = teacher_id
        teacher_id += 1


text = json.dumps(ids, ensure_ascii=False, indent=2)
newIds = open("registro/spiders/profesoresId.json", "w", encoding="utf-8")
newIds.write(text)
newIds.close()


