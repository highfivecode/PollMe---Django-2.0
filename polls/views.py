from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Choice, Poll

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
    """
    Render the poll_detail.html template which allows a user to vote
    on the choices of a poll
    """
    # poll = Poll.objects.get(id=poll_id)
    poll = get_object_or_404(Poll, id=poll_id)

    if request.method == "POST":
        print(request.POST)
        print("YOU POSTED!!!!!!!!!")

    if request.method == "GET":
        print(request.GET)
        print("YOU GET ME!!!!!!!!!!!")

    context = {'poll': poll}
    return render(request, 'polls/poll_detail.html', context)

def poll_vote(request, poll_id):
    # try:
    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        choice.votes += 1
        choice.save()
        return HttpResponse('Poll Id: {}'.format(poll_id))
    return HttpResponse("No Choice Inputted!")
