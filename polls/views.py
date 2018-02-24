from django.shortcuts import render
from django.http import HttpResponse

from .models import Poll

# Create your views here.
def polls_list(request):
    """
    Renders the polls_list.html template which lists all the
    currently available polls
    """
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls/polls_list.html', context)

def poll_detail(request, poll_id):
    return HttpResponse('Youre looking for poll with and id off: {}'.format(poll_id))
