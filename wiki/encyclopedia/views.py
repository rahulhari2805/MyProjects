from django.shortcuts import render

from . import util
import shutil, os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django import forms
from django.db.models import Q

from random import choice
from markdown2 import Markdown

## conversion of markdown to html file and save it to templates folder

def markdown_convert():
    title_html = util.list_entries()
    md = Markdown()
    for title in title_html:
        body = md.convert(util.get_entry(title))
        filename = f"entries/{title}.html"
        if default_storage.exists(filename):
            default_storage.delete(filename)
        default_storage.save(filename, ContentFile("{% extends 'encyclopedia/layout.html' %}" + "\n" + "{% block title %}" + "\n" + 
        title + "\n" + "{% endblock %}" + "\n" + "{% block body %}" + "\n" + "\n" + body + "\n" 
        + "<a href='edit/"+title+"'>Edit Page</a>" + "\n" + "{% endblock %}"))
        shutil.move(f"entries/{title}.html", f"encyclopedia/templates/encyclopedia/{title}.html")




def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random_page": choice(util.list_entries())
    })

def entries(request, entry):
    
    markdown_convert()
    return render(request, f"encyclopedia/{entry}.html", {
        "random_page": choice(util.list_entries())
    })

def search(request):
    results = []
    template = "encyclopedia/search.html"
    
    query = request.GET.get("q")
    
    title_html = util.list_entries()
    
    for words in title_html:
        
        
        if query.lower() == words.lower():
            return HttpResponseRedirect(reverse("entry", kwargs={"entry":words}))

        else:
            word = words.lower()
            result = word.find(query.lower())
            
            if result == 0:
                results.append(words)
                if word == title_html[-1].lower():
                    context = {"results" : results}
                    return render(request, template, context)

    noresult = len(results)
    context1 = {"noresult" : noresult == 0}
    return render(request, template, context1)
    
    
def create(request):
    
    template = "encyclopedia/create.html"
    
    if request.method == "POST":
       
        exist = 0
        title = request.POST.get("title")

        body = request.POST.get("body")
        title_html = util.list_entries()
        
        for words in title_html:
            if title.lower() == words.lower():
                exist = 1
                
        if exist == 1:
            context = {"exist" : exist == 1}
            return render(request, template, context)

        else:
            util.save_entry(title, body)
            markdown_convert()
            return HttpResponseRedirect(reverse("entry", kwargs={"entry":title}))
        

    return render(request, template)

    
   
def edit(request, page_edit):
    filename = f"encyclopedia/templates/encyclopedia/edit/{page_edit}.html"
    f = default_storage.open("encyclopedia/templates/encyclopedia/edit/edit.html")
    filebody = f.read().decode("utf-8")
    
    if default_storage.exists(filename):
        default_storage.delete(filename)

    default_storage.save(filename, ContentFile(filebody))

    template = f"encyclopedia/edit/{page_edit}.html"
    
    title = page_edit
    body = util.get_entry(title)
    
    
    context = {"title" : title, "body" : body}
        
    
    if request.method == "POST":

        edit_title = request.POST.get("edit_title")
        edit_body = request.POST.get("edit_body")
        util.save_entry(edit_title, edit_body)
        default_storage.delete(filename)
        return HttpResponseRedirect(reverse("entry", kwargs={"entry":edit_title}))
        



    return render(request, template, context)








    

   
       
       
    
    

    
        

          
    
    


        
