import pygal
import requests
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    
    context = {
        'title' : 'Home',
    }
    return render(request, 'home.html', context)

def github_repos(request):
   
    response = requests.get('https://api.github.com/users/reginabd/repos')
    context = {
        'title' : 'All Github Repos',
        'repo_data' : response.json()
    }
    return render(request, 'github_repos.html', context)

def github_repo_size(request):
    
    response = requests.get('https://api.github.com/users/reginabd/repos')
    repo_data = response.json()

    
    bars = pygal.HorizontalBar(logarithmic=True)
    bars.title = 'Size of my Github Repositories'
    bars.x_title = 'Size (log scale)'
    bars.y_labels = (1, 5, 10, 50, 100, 500, 1000, 5000)
    for item in repo_data:
        bars.add(item['name'], int(item['size']))

    
    context = {
        'chart' : bars.render_data_uri(),
        'title' : "Github Repo Size",
        }

    
    return render(request, 'github_repo_size.html', context)

def github_repo_languages(request):
 
    username = request.GET.get('username')
    repo_name = request.GET.get('repo_name')

    context = {
        'title' : "Github Languages Used",
    }

 
    if username and repo_name:
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/languages')
        if response.status_code == 200:
         
            context['found'] = True
            context['username'] = username
            context['repo_name'] = repo_name
            
           
            languages_data = response.json()
            pie_chart = pygal.Pie()
            pie_chart.title = 'Github Languages Used in Repo'
            for key, value in languages_data.items():
                pie_chart.add(key, int(value))
            context['chart'] = pie_chart.render_data_uri()
        else:
          
            context['found'] = False
    else:
      
        context['found'] = False
    return render(request, 'github_repo_languages.html', context)