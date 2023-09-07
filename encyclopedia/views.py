from django.shortcuts import render
from . import util
import markdown
import random



def markdownTohtml(title):
    markdowner =markdown.Markdown()
    content=util.get_entry(title)
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
    
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
    
def entry(request, title):
    html_content=markdownTohtml(title)
    if html_content==None:
        return render(request, "encyclopedia/error.html", {'error': "this page is not found"})
    else:
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            'html_content':html_content
            
        })

def search(request):
    if request.method == 'POST':
        search_entry=request.POST['q']
        html_content=markdownTohtml(search_entry)
        if html_content:
             return render(request, "encyclopedia/entry.html", {
            "title":search_entry,
            'html_content':html_content})
        else:
            all_entries=util.list_entries()
            recomand=[]
            for search in all_entries:
                if search_entry.lower() in search.lower():
                    recomand.append(search)
            return render(request, "encyclopedia/search.html", {'recomand': recomand})                     
      
            
def newpage(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/newpage.html")
    else:
        title=request.POST['title']  
        content=request.POST['content']
        isExist=util.get_entry(title)
        if isExist is not None:
            return render(request, "encyclopedia/error.html", {"error": "oops! The page is already exist"})
        else:
            util.save_entry(title, content)
            added_content=markdownTohtml(title)
            return render(request, "encyclopedia/entry.html", {'title':title, 'html_content':added_content})
            
def editpage(request):
    title=request.POST['entry_title']
    content=util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
            "title":title,
            'html_content':content
            
        })
def save_edit(request):
    title=request.POST['title']
    content=request.POST['content']
    util.save_entry(title, content)
    return render(request, "encyclopedia/entry.html", {
            "title":title,
            'html_content':content
        })
    
def random_page(request):
    listOfentry=util.list_entries()
    title=random.choice(listOfentry)
    html_content=markdownTohtml(title)
    return render(request, 'encyclopedia/entry.html', {'title':title, 'html_content':html_content})
    
