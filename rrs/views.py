from django.shortcuts import render
from rrs.utils import prettyPrint as pp
from rrs.recommedation_pojo import Recommedation
from rrs.restaurant_recommender import Restaurant_Recommender
from rrs.tf_idf import TF_IDF
from .forms import NameForm


def index(request):
    pp("index called")
    context = {}
    form = NameForm()
    recommondationsNotAvail = False

    if request.method == 'POST':
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form_sentence = form.cleaned_data["sentence"]
            form_cuisine = form.cleaned_data["cuisine"]
            form_city = form.cleaned_data["city"]
            model = TF_IDF(form_city)
            topNRecommendations = model.produce_recommendations(
                form_sentence, 10)
            pp(form_sentence)
            pp(form_cuisine)
            if form_cuisine == "none":
                # a list of restaurant objects
                context = {"topNRecommendations": topNRecommendations}
            else:
                recommedations = cusine_process(
                    topNRecommendations, form_cuisine)
                if recommedations == []:
                    recommondationsNotAvail = True
                context = {"topNRecommendations": recommedations}

            context['range'] = range(5)
            context['recommondationsNotAvail'] = recommondationsNotAvail
            form = NameForm()

    context['form'] = form

    return render(request, 'rrs/main.html', context)


def cusine_process(topNRecommendations, cuisine):
    recomm = []
    pp("Cuisine_process id called")
    pp(cuisine)
    # Select each object from the recommendation list
    for topr in topNRecommendations:
        # select the category
        for cat in topr.cuisine:
            if cuisine == cat:
                recomm.append(topr)
    print(recomm)
    return recomm


def model(request):
    print("rss/model running.....")

    return render(request, 'rrs/model.html', context={})


def map(request, city, rest_name):
    print("map loading.....")
    print(rest_name)
    recom = Restaurant_Recommender(city)
    recom.train_test_split()
    recom.get_recommendations(rest_name)
    return render(request, 'rrs/map.html', context={})
