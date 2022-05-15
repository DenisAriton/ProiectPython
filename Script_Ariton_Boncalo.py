"""
Nume studenti : Ariton Denis-Adrian si Boncalo Sebastian

Nume proiect : Parcurgerea unor documente pentru a extrage informația cerută

Cerinte : Dezvoltați un script care să permită extragerea recenziilor de la o anumită adresa și salvarea lor
                                                                                                într-un document json.

    1) Extrageti recenziile (reviews) de la adresa:
                https://www.goodreads.com/book/show/4214.Life_of_Pi#CommunityReviews
                https://www.goodreads.com/book/show/4214.Life_of_Pi?language_code=en&page={i}
    2)Pentru fiecare recenzie extrageți autor, data, text recenzie.

    3)Salvați recenziile extrase într-un document json.
"""
import requests
from bs4 import BeautifulSoup
import json
import os
def get_soup(url):
     download=requests.get(url) #descarcam continutul paginii de la adresa url
     supa=BeautifulSoup(download.content,'html.parser')#apelam constructorul pentru parcurgerea site-ului
     return supa

def get_reviews(supa):
     reviews=supa.find_all('div',{'class':'friendReviews elementListBrown'})#extragem doar div-urile care contin partea de review-uri

     try:
          # parcurgem codul html stocat in reviews pentru a extrage urmatoarele date : autor,data,text comentariu
          reviewlist=list()
          for el in reviews:
              date_procesate={
               'Autor recenzie': el.find('a',{'class':'user'}).text,
               'Data publicarii recenziei': el.find('a',{'class':'reviewDate createdAt right'}).text,
               'Textul recenziei': el.find('div',{'class':'reviewText stacked'}).text.strip()
               }
              reviewlist.append(date_procesate)
          return reviewlist
     except Exception as e:
          print(f'Eroarea este : {e}')

date_extrase=list()
j=0
# navigam pe fiecare pagina web a cartii Life of Pi si extragem pentru fiecare pagina recenziile apeland functiile
#verificam prin if daca s-au gasit recenzii , deoarece printr-o singura incercare este posibil sa nu gaseasca nicio recenzie si trece mai departe
for i in range(1,11):
    supa = get_soup(f'https://www.goodreads.com/book/show/4214.Life_of_Pi?language_code=en&page={i}')
    if len(get_reviews(supa))==0  :
        supa = get_soup(f'https://www.goodreads.com/book/show/4214.Life_of_Pi?language_code=en&page={i}')
        date_extrase.extend(get_reviews(supa))
    else:
        date_extrase.extend(get_reviews(supa))
    print(f'Pagina {i} are {len(date_extrase)} de recenzii\n')
# creare fisier json
if not os.path.isdir('Fisier_Json'):
    os.mkdir('Fisier_Json') #cream un folder unde se va stoca fisierul json
with open('Fisier_Json/date_extrase.json','w+') as out:
    json.dump({'Datele extrase sunt ':date_extrase},out,indent=4)
