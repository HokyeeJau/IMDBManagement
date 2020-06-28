from django.shortcuts import render
from django.http import HttpResponse
from . import connect_db
from . import search
import re
actors = connect_db.get_actor()

def main(request):
    return render(request, 'main.html')

# Actor Page
def actor(request):
    actors = connect_db.get_actor()
    items = []
    i = 0
    for actor in actors:
        item = "<tr><td><label><input type='radio' name='actor' value='"+str(actor['id'])+"' />"+str(actor['id'])+"</label></td><td>"+actor['fir']+"</td><td>"+actor['sec']+"</td><td>"+actor['gender']+"</td><td>"+" ".join(actor['movies'])+"</td></tr>"
        items.append(item)
        i = i + 1
    context = {}
    context['actor_list'] = items
    # context['hello'] = 'Hello World!'
    return render(request, 'actor.html', context)

# Filter Actor Function (Return Actor Page)
def filter_actor(request):
    actors = connect_db.filter_actor(request)
    items = []
    i = 0
    for actor in actors:
        item = "<tr><td><label><input type='radio' name='actor' value='"+str(actor['id'])+"' />"+str(actor['id'])+"</label></td><td>"+actor['fir']+"</td><td>"+actor['sec']+"</td><td>"+actor['gender']+"</td><td>"+" ".join(actor['movies'])+"</td></tr>"
        items.append(item)
        i = i + 1
    context = {}
    context['actor_list'] = items
    actors = items
    # context['hello'] = 'Hello World!'
    return render(request, 'actor.html', context)

# Edit Actor Page
def edit_actor(request):
    request.encoding='utf-8'

    genders = ['M', 'F']
    row = ''
    if 'actor' in request.GET and request.GET['actor']:
        num = int(request.GET['actor'])
    actor = connect_db.return_actor(num)

    mod_input = "<label>ID: <input name='id' type='text' value='"+str(actor.id)+"' readonly='readonly' /></label><br /><label>First Name: <input type='text' name='fir' value='"+actor.fir_name+"'/></label><br /><label>Second Name: <input type='text' name='sec' value='"+actor.sec_name+"'/></label><br />"
    select_group = "Gender: <select name='gender'>"
    for gender in genders:
        if gender == actor.gender:
            select_group = select_group + "<option value='"+gender+"' selected='seleted'>"+gender+"</option>"
        else:
            select_group = select_group + "<option value='"+gender+"'>"+gender+"</option>"
    select_group = select_group + "</select><br />"

    select_group = select_group + "Movie: <select name='movie'>"
    # movie_name = connect_db.return_movie_name(num)
    for name in connect_db.all_movie_name():
        select_group = select_group + "<option value='"+name+"'>"+name+"</option>"
    select_group = select_group+"</select>"
    context = {}
    context['mod_input'] = mod_input + select_group
    context['delete'] = 'adelete'
    context['modify'] = 'amodify'
    context['actor'] = num
    return render(request, 'edit.html', context)

# Delete Actor Page
def delete_actor(request):
    item = -1
    if 'actor' in request.POST and request.POST['actor']:
        item = actors[int(request.POST['actor'])]
    if connect_db.delete_actor(item['id']) == 1:
        return HttpResponse('Delete Successfully')

# Modify Actor Page
def modify_actor(request):
    item = -1
    ctx = {}
    if 'id' in request.POST and request.POST['id']:
        ctx['id'] = request.POST['id']
        ctx['fir'] = request.POST['fir']
        ctx['sec'] = request.POST['sec']
        ctx['gender'] = request.POST['gender']
        ctx['movie'] = request.POST['movie']
        connect_db.modify_actor(ctx)
    return HttpResponse('Modify Successfully')

# Add Actor Page
def add_apointer(request):
    genders = ['M', 'F']
    add_input = "<label>ID: <input name='id' type='text' value='' /></label><br /><label>First Name: <input type='text' name='fir' value=''/></label><br /><label>Second Name: <input type='text' name='sec' value=''/></label><br />"
    select_group = "Gender: <select name='gender'>"
    for gender in genders:
        select_group = select_group + "<option value='"+gender+"'>"+gender+"</option>"
    select_group = select_group + "</select><br />"

    select_group = select_group + "Movie: <select name='movie'>"
    for name in connect_db.all_movie_name():
        select_group = select_group + "<option value='"+name+"'>"+name+"</option>"
    select_group = select_group+"</select>"
    context = {}
    context['add_input'] = add_input+select_group+"<br /><label>role: <input name='role' type='text' value='' /></label>"
    context['add'] = 'aadd'
    return render(request, 'add.html', context);

# Add Response
def add_actor(request):
    back = connect_db.add_actor(request)
    if back == 1:
        return HttpResponse('Add Successfully')
    else:
        return HttpResponse('Error')

# Director Page
def director(request):
    dirs = connect_db.get_director()
    # return HttpResponse(dirs)
    items = []
    i = 0
    for dir in dirs:
        movies = connect_db.get_director_movies(dir['id'])
        item = "<tr><td><label><input type='radio' name='dir' value='"+str(dir['id'])+"' />"+str(dir['id'])+"</label></td><td>"+dir['fir']+"</td><td>"+dir['sec']+"</td><td>"+" ".join(movies)+"</td></tr>"
        items.append(item)
        i = i + 1
    context = {}
    context['director_list'] = items
    return render(request, 'director.html', context)

# Filter Director Page
def filter_director(request):
    directors = connect_db.filter_director(request)
    items = []
    i = 0
    for dirs in directors:
        movies = connect_db.get_director_movies(dirs['id'])
        item = "<tr><td><label><input type='radio' name='dir' value='"+str(dirs['id'])+"' />"+str(dirs['id'])+"</label></td><td>"+dirs['fir']+"</td><td>"+dirs['sec']+"</td><td>"+" ".join(movies)+"</td></tr>"
        items.append(item)
        i = i + 1
    context = {}
    context['director_list'] = items
    return render(request, 'director.html', context)

# Edit Director Page
def edit_director(request):
    request.encoding='utf-8'
    row = ''
    if 'dir' in request.GET and request.GET['dir']:
        num = int(request.GET['dir'])
    d = connect_db.return_director(num)

    mod_input = "<label>ID: <input name='id' type='text' value='"+str(d.id)+"' readonly='readonly' /></label><br /><label>First Name: <input type='text' name='fir' value='"+d.fir_name+"'/></label><br /><label>Second Name: <input type='text' name='sec' value='"+d.sec_name+"'/></label><br />"

    select_group = "<label>Movies: </label><br />"
    i = 0
    for name in connect_db.all_movie_name():
        if i != 0 and i % 3 == 0:
            select_group = select_group + "<br />"
        if name in connect_db.get_director_movies(num):
            select_group = select_group + "<label><input type='checkbox' name='movies' value='"+name+"' checked='checked' />"+name+"</label>"
        else:
            select_group = select_group + "<label><input type='checkbox' name='movies' value='"+name+"' />"+name+"</label>"
        i += 1
    context = {}
    context['mod_input'] = mod_input + select_group
    context['delete'] = 'ddelete'
    context['modify'] = 'dmodify'
    context['id'] = num
    return render(request, 'edit.html', context)

# Delete Director Page
def delete_director(request):
    item = -1
    if 'id' in request.POST and request.POST['id']:
        idx = int(request.POST['id'])
    if connect_db.delete_director(idx) == 1:
        return HttpResponse('Delete Successfully')

# Modify Director Page
def modify_director(request):
    ctx = {}
    if 'id' in request.POST and request.POST['id']:
        ctx['id'] = request.POST['id']
        ctx['fir'] = request.POST['fir']
        ctx['sec'] = request.POST['sec']
        ctx['movies'] = request.POST['movies']
        connect_db.modify_director(ctx)
    return HttpResponse('Modify Successfully')

# Add Director Page
def add_dpointer(request):
    add_input = "<label>ID: <input name='id' type='text' value='' /></label><br /><label>First Name: <input type='text' name='fir' value=''/></label><br /><label>Second Name: <input type='text' name='sec' value=''/></label><br />"

    select_group = "Movie: <select name='movie'>"
    for name in connect_db.all_movie_name():
        select_group = select_group + "<option value='"+name+"'>"+name+"</option>"
    select_group = select_group+"</select>"
    context = {}
    context['add_input'] = add_input+select_group
    context['add'] = 'ddadd'
    return render(request, 'add.html', context);

# Add Response
def add_director(request):
    back = connect_db.add_director(request)
    if back == 1:
        return HttpResponse('Add Successfully')
    else:
        return HttpResponse('Error')

# Movie Page
def movie(request):
    movies = connect_db.get_movie()
    # return HttpResponse(dirs)
    items = []
    i = 0
    for m in movies:
        item = "<tr><td><label><input type='radio' name='mov' value='"+str(m['id'])+"' />"+str(m['id'])+"</label></td><td>"+m['name']+"</td><td>"+str(m['year'])+"</td><td>"+str(m['rank'])+"</td><td>"+str(m['director'])+"</td></tr>"
        items.append(item)
        i = i + 1
    context = {}
    context['movie_list'] = items
    return render(request, 'movie.html', context)

# Filter Movie Page
def filter_movie(request):
    movies = connect_db.filter_movie(request)
    items = []
    i = 0
    for m in movies:
        item = "<tr><td><label><input type='radio' name='mov' value='"+str(m['id'])+"' />"+str(m['id'])+"</label></td><td>"+m['name']+"</td><td>"+str(m['year'])+"</td><td>"+str(m['rank'])+"</td><td>"+str(m['director'])+"</td></tr>"
        items.append(item)
        i = i + 1
    context = {}
    context['movie_list'] = items
    return render(request, 'movie.html', context)

# Edit Movie Page
def edit_movie(request):
    request.encoding='utf-8'
    row = ''
    if 'mov' in request.GET and request.GET['mov']:
        num = int(request.GET['mov'])
    m = connect_db.return_movie(num)

    mod_input = "<label>ID: <input name='mov' type='text' value='"+str(m.id)+"' readonly='readonly' /></label><br /><label>Movie Name: <input type='text' name='name' value='"+m.name+"'/></label><br /><label>Publish Year: <input type='text' name='year' value='"+str(m.year)+"'/></label><br /><label>Publish Rank: <input type='text' name='rank' value='"+str(m.rank)+"'/></label><br />"

    select_group = "Director ID<select name='did'>"
    dir_id_name = connect_db.return_dir_list()
    for din in dir_id_name:
        select_group = select_group + "<option value='"+str(din[0])+"'>"+din[1]+"</option>"
    select_group = select_group + "</select><br />"
    context = {}
    context['mod_input'] = mod_input + select_group
    context['delete'] = 'mdelete'
    context['modify'] = 'mmodify'
    context['id'] = num
    return render(request, 'edit.html', context)

# Delete Movie Page
def delete_movie(request):
    # return HttpResponse('Test')
    if 'id' in request.POST and request.POST['id']:
        idx = int(request.POST['id'])
    if connect_db.delete_movie(idx) == 1:
        return HttpResponse('Delete Successfully')

# Modify Movie Page
def modify_movie(request):
    # return HttpResponse('Test')
    ctx = {}
    if 'id' in request.POST and request.POST['id']:
        ctx['id'] = request.POST['id']
        ctx['name'] = request.POST['name']
        ctx['year'] = request.POST['year']
        ctx['rank'] = request.POST['rank']
        ctx['did'] = request.POST['did']
        connect_db.modify_movie(ctx)
    return HttpResponse('Modify Successfully')

# Add Movie Page
def add_mpointer(request):
    add_input = "<label>ID: <input name='mov' type='text' value='' /></label><br /><label>Name: <input type='text' name='name' value=''/></label><br /><label>Year: <input type='text' name='year' value=''/></label><br /><label>Rank: <input type='text' name='rank' value=''/></label><br />"

    select_group = "Director ID<select name='did'>"
    dir_id_name = connect_db.return_dir_list()
    for din in dir_id_name:
        select_group = select_group + "<option value='"+str(din[0])+"'>"+din[1]+"</option>"
    select_group = select_group + "</select><br />"

    context = {}
    context['add_input'] = add_input+select_group
    context['add'] = 'mmadd'
    return render(request, 'add.html', context);

# Add Response
def add_movie(request):
    back = connect_db.add_movie(request)
    if back == 1:
        return HttpResponse('Add Successfully')
    else:
        return HttpResponse(str(back))
