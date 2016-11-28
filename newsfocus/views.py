import json
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
#from search_news import search_by_category, search_by_all
from search_articles import search_by_keywords
from django.http import JsonResponse
from django.views.generic import View

# Create your views here.
class results(View):
	#used when click on fields grids
	#no longer be used
	def get(self, request, *args, **kwargs):
		category = request.GET.get('category', '')
		results = search_by_category(ctg=category)
		return render(request, 'newsfocus/results.html', {'results': results})

	#this function only be used when search in first page
	def post(self, request, *args, **kwargs):
		keywords = request.POST.get('keywords')
		# keywords = request.POST.get('keywords')
		# categories = request.POST.getlist('categories')
		# daterange = request.POST.get('daterange')
		# results = search_by_all(keywords=keywords, ctg=categories, daterange=daterange)
		results = keywords
		return render(request, 'newsfocus/results.html', {'results': results})

#function name is url name
def index(request):
	lst = ['art', 'business', 'food', 'health', 'science', 'travel', 'sports', 'world']
	return render(request, 'newsfocus/index.html', {'name_lst': lst})

#function name is url name
#found in ajax_search.js
#we only use this ordinary_search when search in second page (result)
def ordinary_search(request):
	keywords = request.POST.get("keywords")
	results = search_by_keywords(keywords=keywords)
	return JsonResponse(results, safe=False)

