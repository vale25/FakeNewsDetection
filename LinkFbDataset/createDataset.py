import csv
from boilerpipe.extract import Extractor
from unidecode import unidecode

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))


writer = csv.writer(open('/home/luca/Documenti/Tesi/Facebook_dataset.csv', 'w'))
f = open ('/home/luca/Documenti/Tesi/facebook-fact-check-edited.csv', 'r')
reader = csv.reader(f)
#Foreach news catch link and extract html content
for row in reader:
    line = row[1]
    print(line)
    try:
        extractor = Extractor(extractor='ArticleExtractor', url=line)
        extracted_text = extractor.getText()
        if extracted_text != "" or extracted_text != None:
            html_news = extracted_text.encode("utf-8")
            row.append(html_news)
            writer.writerow(row)
    except:
        print("exception")

f.close()