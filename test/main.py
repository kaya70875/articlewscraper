from data import refactor
from scripts import word_algo
from test.spiders import scienceSpider , newsSpider , psySpider

# ÇEKTİĞİMİZ BÜTÜN TEXTLERİ DATA KLASÖRÜ ALTINDA KENDİ İSİLERİ VE KATEGORİLERİ İLE SINIFLANDIRABİLİRİZ. MAİN FİLE İÇERİSİNDE 'TEXT' HESAPLAMASI YAPMAKTANSA BU HESAPLAMALARI BAŞKA
# KLASOR VEYA FONKSİYONLARA ATAYABİLİRİZ. BURADAN İSTEDİĞİMİZ KATEGORİ İLE İLGİLİ KELİMELERİ ÇEKEBİLİRİZ(KARIŞIK NASIL YAPARIZ DÜŞÜN). YARIN BUNUN İÇİN UĞRAŞ

#run spider : 
update = str(input('Do you want to update database : '))
if update == ('y'):
    scienceSpider.process.start()
    newsSpider.process.start()
    psySpider.process.start()

science = refactor.get_science()
news = refactor.get_news()
psy = refactor.get_psy()

word = word_algo.create_topics([science , news , psy] , input('Word : '))
#word = word_algo.create_sentence(psy, input('Word : '))

for i , sentence in enumerate(word):
    
    print(f'Sentence {i + 1} : {sentence}')
