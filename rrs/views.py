from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
from rrs.colab.cnbf import content_based_filtering
from rrs.colab.ml3 import collaborititveFiltering
from rrs.colab.utils import prettyPrint as pp
from rrs.colab.datapreprocessing import data_preprocessing
df_final = pd.DataFrame()
################## LOAD DATASET #####################
pp("Loading Dataset")
# Define path for dataset
business_data_path = "C:/Users/Midhun/Downloads/yelp_academic_dataset_business.json"
reviews_data_path = "C:/Users/Midhun/Downloads/yelp_academic_dataset_review.json"

# import the data (chunksize returns jsonReader for iteration)
businesses = pd.read_json(business_data_path, lines=True,
                          orient='columns', chunksize=1000000)
reviews = pd.read_json(reviews_data_path, lines=True,
                       orient='columns', chunksize=1000000)

for business in businesses:
    df_business = business
    break

for review in reviews:
    df_review = review
    break
pp("Dataset Loaded")
print(df_business.head())
print(df_review.head())
################## END LOAD DATASET #####################


################## DATA PREPROCESSING #####################


################## VIEW METHODS #####################


def index(request):
    global df_final
    pp("Started Datapreprocessing")
    if len(df_final.index) == 0:
        df_final = data_preprocessing(df_business)
        pp("Datapreprocessing Successful")
    return render(request, 'rrs/main.html')


def model(request):
    print("rss/model running.....")
    # post
    # result = run('Village Whiskey', 10)
    cnbf_result = content_based_filtering(df_final)
    print(cnbf_result)
    # cnbf_result = collaborititve_filtering()
    # context = {'result': cnbf_result}
    return render(request, 'rrs/model.html', context={})
