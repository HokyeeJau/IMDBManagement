from article.models import *
from . import connect_db

def filter_actor(request):
    actor = connect_db.get_actor()
    request.encoding='utf-8'

    if 'id' in request.GET and request.GET['id']:
        for row in actor:
            if int(actor['id']) == int(request.GET['id']):
                return row
        return {}

    filt1 = []
    if 'fir' in request.GET and request.GET['fir']:
        for row in actor:
            if row['fir'].find(request.GET['fir']) != -1:
                filt1.append(row)

    filt2 = []
    if 'sec' in request.GET and request.GET['sec']:
        for row in filt1:
            if row['sec'].find(request.GET['sec']) != -1:
                filt2.append(row)

    filt3 = []
    if 'gender' in request.GET and request.GET['gender']:
        for row in filt2:
            if row['gender'] == request.GET['gender']:
                filt3.append(row)

    items = []
    i = 0
    for actor in filt3:
        item = "<tr><td>"+str(actor['id'])+"</td><td>"+actor['fir']+"</td><td>"+actor['sec']+"</td><td>"+actor['gender']+"</td><td>"+" ".join(actor['movies'])+"</td><td><button type='button'>Modify</button></td><td><button type='button'>Delete</button></td></tr>"
        items.append(item)
        i = i + 1
    context = {}
    context['actor_list'] = items
    # context['hello'] = 'Hello World!'
    return render(request, 'actor.html', context)
