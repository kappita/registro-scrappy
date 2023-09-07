call scrapy crawl facultades -o facultades.json
call scrapy crawl carreras -o carreras.json

call scrapy crawl profesores -o profesores.json
call python indexTeachers.py
call scrapy crawl registro -o registro.json
call 
PAUSE