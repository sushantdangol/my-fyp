from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

import json
from rouge import Rouge 

from core.summarize_service import generate_summary
from core.scraper import scraper

from core.models import InputText, WebScrape
from core.forms import InputForm, WebScrapeForm

# Create your views here.
def index(self):
    input_text = InputText.objects.all().order_by('-pub_date')
    # result = generate_summary(input_text.content, 3)
    template = loader.get_template('core/index.html')
    
    # input_text.summary = result
    # input_text.save()

    # context = {
    #     'summary': input_text.summary,
    #     'original': input_text.content,
    #     'title': input_text.title
    # }

    return HttpResponse(template.render({'index': input_text}))

def post_input(request):
    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            score = []

            result = generate_summary(content, 3)

            #calculate the rouge score
            rouge = Rouge()
            
            scores = rouge.get_scores(content, result)

            a = InputText(title=title, content=content, summary=result, rouge=scores)

            a.save()    

 
            print(scores)

            return HttpResponseRedirect("/index/")

    else:
        form = InputForm()

    
    return render(request, 'core/input.html', {'form': form})

def web_scrape(request):
    if request.method == 'POST':
        form = WebScrapeForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            story = scraper(url)
            
            b = WebScrape(url = url, story = story)
            b.save()
            
            result = generate_summary(b.story)
            a = InputText(title="From Kathmandu Post", content=story, summary=result)
            a.save()

            return HttpResponseRedirect("/index/")

    else:
        form = WebScrapeForm()

    return render(request, 'core/url.html', {'form': form})
    






            







