from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

mydata = pd.read_json("/home/luca/PycharmProjects/FakeNewsDetection/K-means_model/trainset_senza_duplicati.json", lines=True)
df = pd.DataFrame(mydata)
real = df.loc[df['label'] == "REAL"]
fake = df.loc[df['label'] == "FAKE"]
#print(real)
real_text = real["text"][:500]
fake_text = fake["text"][:500]
print(real_text)
real_text.to_pickle("real_news")
fake_text.to_pickle("fake_news")
#real_text.to_csv("realnews_csv", sep='\t', encoding='utf-8')
#fake_text.to_csv("fakenews_csv", sep='\t', encoding='utf-8')


'''input_file=open('/home/luca/PycharmProjects/FakeNewsDetection/Neural_networks/trainset_senza_duplicati.json', 'r')
output_file=open('test.json', 'w')
json_decode=json.load(input_file)
result = []
for item in json_decode:
    if(item.get('label')=='REAL'):
        my_dict={}
        my_dict['text']=item.get('text')
        my_dict['label']=item.get('label')
        my_dict['id']=item.get('id')
        my_dict['title']= item.get('title')
        print my_dict
        result.append(my_dict)
back_json=json.dumps(my_dict, output_file)
output_file.write(back_json)
output_file.close()'''