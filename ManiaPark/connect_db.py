from django.http import HttpResponse

from article.models import *

# 数据库操作
def all_actor():
    return actors.objects.all()

def all_movie():
    return movies.objects.all()

def all_director():
    return directors.objects.all()

def all_movie_name():
    n = []
    for m in all_movie():
        n.append(m.name)
    return n;

def return_movie_name(id):
    movie_id = roles.objects.filter(actor_id=id).first().movie_id
    movie_names = movies.objects.filter(id=movie_id)
    movie_name = []
    for name in movie_names:
        movie_name.append(str(name.name))
    return " ".join(movie_name) 

def return_actor(id):
    return actors.objects.filter(id=id).first()

def return_director(id):
    return directors.objects.filter(id=id).first()

def return_movie(id):
    return movies.objects.filter(id=id).first()

def return_dir_list():
    mdir = directors.objects.all()
    id_name = []
    for idx in mdir:
        id_name.append([idx.id, idx.fir_name+" "+idx.sec_name])
    return id_name

def get_director_movies(id):
    movie_ids = movie_director.objects.filter(director_id=id)
    mov = []
    for idx in movie_ids:
        movie_name = movies.objects.filter(id=idx.movie_id).first().name
        mov.append(movie_name)
    return mov

# Actors
def get_actor(Actors=0):
    if Actors == 0:
        Actors = all_actor();

    actor = []
    for a in Actors:
        item = {'id': a.id,
                'fir':a.fir_name,
                'sec':a.sec_name,
                'gender':a.gender,
                'movies':[]}
        role = roles.objects.filter(actor_id=a.id)
        for r in role:
            movie = movies.objects.filter(id=r.movie_id).first()
            item['movies'].append(movie.name)
        actor.append(item)
    return actor;

def filter_actor(request):
    actors = all_actor()
    request.encoding='utf-8'

    if 'id' in request.GET and request.GET['id']!="":
        actors = actors.filter(id=request.GET['id'])

    if 'fir' in request.GET and request.GET['fir']!="":
        actors = actors.filter(fir_name=request.GET['fir'])

    if 'sec' in request.GET and request.GET['sec']!="":
        actors = actors.filter(sec_name=request.GET['sec'])

    if 'gender' in request.GET and request.GET['gender']!="":
        actors = actors.filter(gender=request.GET['gender'])
    return get_actor(actors)

def delete_actor(id):
    test = actors.objects.get(id=id)
    test.delete()
    test = roles.objects.get(actor_id=id)
    test.delete()
    return 1

def modify_actor(ctx):
    text = actors.objects.filter(id=ctx['id']).first()
    text.fir_name = ctx['fir']
    text.sec_name = ctx['sec']
    text.gender = ctx['gender']
    text.save()

    m = movies.objects.filter(name=ctx['movie']).first()
    r = roles.objects.filter(movie_id=m.id).first()

    r.movie_id = m.id
    r.role = ""
    r.save()

def add_actor(request):
    request.encoding='utf-8'
    if 'id' in request.POST and request.POST['id'].isdigit():
        id = request.POST['id']
    else:
        return -1

    if 'fir' in request.POST and request.POST['fir']:
        fir =  request.POST['fir']
    else:
        return -2

    if 'sec' in request.POST and request.POST['sec']:
        sec = request.POST['sec']
    else:
        return -3

    if 'gender' in request.POST and request.POST['gender']:
        gender = request.POST['gender']
    else:
        return -4

    if 'movie' in request.POST and request.POST['movie']:
        m = movies.objects.filter(name=request.POST['movie']).first()
    else:
        return -5

    if 'role' in request.POST and request.POST['role']:
        role = request.POST['role']
    else:
        return -6

    test = actors(id=id,fir_name = fir,sec_name = sec,gender = gender)
    test.save()
    test = roles(actor_id=id,movie_id=m.id,role=role)
    test.save()
    return 1

# Directors
def get_director(dirs=0):
    if dirs == 0:
        dirs = all_director()

    director = []
    for d in dirs:
        item = {'id': d.id,
                'fir':d.fir_name,
                'sec':d.sec_name
                }
        director.append(item)
    return director;

def filter_director(request):
    director = all_director()
    request.encoding='utf-8'

    if 'id' in request.GET and request.GET['id']!="":
        director = director.filter(id=request.GET['id'])

    if 'fir' in request.GET and request.GET['fir']!="":
        director = director.filter(fir_name=request.GET['fir'])

    if 'sec' in request.GET and request.GET['sec']!="":
        director = director.filter(sec_name=request.GET['sec'])

    if 'mov' in request.GET and request.GET['mov']!="":
        movie = movies.objects.filter(name=request.GET['mov']).first()
        dir_id = movie_director.objects.filter(movie_id=movie.id).first()
        director = director.filter(id=dir_id)
    return get_director(director)

def delete_director(id):
    # Delete Director
    dirs = director.objects.filter(id=id).first()
    # Delete Movie
    movie_id = movie_director.objects.filter(director_id=dirs.id)
    # Delete Roles
    for idx in movie_id:
         role = roles.objects.filter(movie_id=idx.id)
         role.delete()
    movid_id.delete()
    dirs.delete()
    return 1


def modify_director(ctx):
    text = directors.objects.filter(id=ctx['id']).first()
    text.fir_name = ctx['fir']
    text.sec_name = ctx['sec']
    text.save()
    all_movies = []

    for m in all_movie():
        mname = m.name 
        movie_id = movies.objects.get(name=m).id
        # Add Movie Director
        if mname in ctx['movies']:
            if movie_director.objects.filter(movie_id=movie_id).filter(director_id=ctx['id']).count() == 0:
                m = movie_director(movie_director=movie_id, director_id=ctx['id'])
                m.save()
        # Delete Movie Director
        else:
            exists = movie_director.objects.filter(movie_id=movie_id).filter(director_id=ctx['id'])
            exists.delete()

def add_director(request):
    request.encoding='utf-8'
    if 'id' in request.POST and request.POST['id'].isdigit():
        id = request.POST['id']
    else:
        return -1

    if 'fir' in request.POST and request.POST['fir']:
        fir =  request.POST['fir']
    else:
        return -2

    if 'sec' in request.POST and request.POST['sec']:
        sec = request.POST['sec']
    else:
        return -3

    if 'movie' in request.POST and request.POST['movie']:
        m = movies.objects.filter(name=request.POST['movie']).first()
    else:
        return -4

    test = directors(id=id,fir_name = fir,sec_name = sec)
    test.save()
    movie_id = movies.objects.get(name=m.name).id

    test = movie_director(director_id=id,movie_id=movie_id)
    test.save()
    return 1

# Movies
def get_movie(mov=0):
    if mov == 0:
        mov = movies.objects.all()
    
    movie = []
    for m in mov:
        did = movie_director.objects.filter(movie_id=m.id).first().director_id
        d = directors.objects.get(id=did)
        item = {
            'id':m.id,
            'name':m.name,
            'year':m.year,
            'rank':m.rank,
            'director': d.fir_name+" "+d.sec_name
        }
        movie.append(item)
    return movie

def filter_movie(request):
    movie = all_movie()
    request.encoding='utf-8'

    if 'id' in request.GET and request.GET['id']!="":
        movie = movie.filter(id=request.GET['id'])

    if 'name' in request.GET and request.GET['name']!="":
        movie = movie.filter(name=request.GET['name'])

    if 'year' in request.GET and request.GET['year']!="":
        movie = movie.filter(year=request.GET['year'])

    return get_movie(movie)

def delete_movie(id):
    # Delete Movie
    mov = movies.objects.filter(id=id)

    # Delete Director
    director_id = movie_director.objects.filter(movie_id=mov.id)

    # Delete Roles
    for idx in mov:
         role = roles.objects.filter(movie_id=idx.id)
         role.delete()

    director_id.delete()
    mov.delete()
    return 1

def modify_movie(ctx):
    # Add movie
    mov = movies(id=ctx['id'], name=ctx['name'], year=ctx['year'], rank=ctx['year'])
    mov.save()
    all_movies = []

    # Delete the original movie-director mapping
    mov_dir = movie_director.objects.filter(id=ctx['id'])
    mov_dir.delete()

    # Build new movie-director mapping
    mov_dir = movie_director(director_id=ctx['did'], movie_id=ctx['id'])
    mov_dir.save()


def add_movie(request):
    request.encoding='utf-8'
    if 'mov' in request.POST and request.POST['mov'].isdigit():
        mid = request.POST['mov']
    else:
        return -1

    if 'name' in request.POST and request.POST['name']:
        name =  request.POST['name']
    else:
        return -2

    if 'year' in request.POST and request.POST['year']:
        year = request.POST['year']
    else:
        return -3

    if 'rank' in request.POST and request.POST['rank']:
        rank = request.POST['rank']
    else:
        return -4

    if 'did' in request.POST and request.POST['did']:
        did = request.POST['did']
    else:
        return -5

    test = movies(id=mid, name=name, year=year, rank=rank)
    test.save()

    test = movie_director(director_id=did,movie_id=mid)
    test.save()
    return 1
