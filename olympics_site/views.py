from django.shortcuts import render
from django.http import HttpResponse
from json import dumps
import urllib.request
from bs4 import BeautifulSoup
from olympics_site.models import MedalTable

def webscrapper():
    wikiUrl = 'https://en.wikipedia.org/wiki/2018_Winter_Olympics_medal_table'
    wikiPage = urllib.request.urlopen(wikiUrl)
    soup = BeautifulSoup(wikiPage,"html.parser",from_encoding="UTF-8")
    table = soup.find("table", { "class" : "wikitable sortable plainrowheaders" })
    rows = table.findChildren('tr')[1:-1]
    previous_rank = 1
    MedalTable.objects.all().delete()
    for row in rows:
        row_data = row.findChildren(['th','td'])
        
        if len(row_data) < 6:
            final_rank = previous_rank
            base_index = - 1
        else:
            final_rank =  int(row_data[0].text)
            previous_rank=final_rank
            base_index = 0
        
        MedalTable.objects.create(rank=final_rank, country=row_data[base_index+1].findChildren('a')[0].text,
                                  gold=int(row_data[base_index+2].text), silver=int(row_data[base_index+3].text),
                                  bronze=int(row_data[base_index+4].text), total=int(row_data[base_index+5].text)) 
            
def medal_data_list(request):
    webscrapper()
    medals_table = MedalTable.objects.order_by('rank')
    return render(request, 'olympics_site/base.html', {"medals_data":medals_table})
    
    
def analytics_data(request):
    dataset = MedalTable.objects.order_by('rank')
    country_list = list()
    gold_medal_list = list()
    silver_medal_list = list()
    bronze_medal_list = list()
    #pdb.set_trace()
    for data in dataset:
        country_list.append(data.country)
        gold_medal_list.append(data.gold)
        silver_medal_list.append(data.silver)
        bronze_medal_list.append(data.bronze)
    return HttpResponse(
                        dumps({"country":country_list,
                              "gold":gold_medal_list,
                              "silver":silver_medal_list,
                              "bronze":bronze_medal_list}),
                        content_type="application/json"
                    )

