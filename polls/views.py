from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

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
    context = {'poll': poll}
    return render(request, 'polls/poll_detail.html', context)

def poll_vote(request, poll_id):
    # try:
    poll = get_object_or_404(Poll, id=poll_id)
    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        choice.votes += 1
        choice.save()
    else:
        messages.error(request, 'No Choice Was Found!')
    return render(request, 'polls/poll_results.html', {'poll': poll})
