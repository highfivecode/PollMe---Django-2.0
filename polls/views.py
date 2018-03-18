import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Choice, Poll, Vote

from .forms import PollForm, EditPollForm, ChoiceForm

# Create your views here.
@login_required
def polls_list(request):
    """
    Renders the polls_list.html template which lists all the
    currently available polls
    """
    polls = Poll.objects.all()
    context = {'polls': polls}
    return render(request, 'polls/polls_list.html', context)

@login_required
def add_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            new_poll = form.save(commit=False)
            new_poll.pub_date = datetime.datetime.now()
            new_poll.owner = request.user
            new_poll.save()
            new_choice1 = Choice(
                                    poll = new_poll,
                                    choice_text=form.cleaned_data['choice1']
                                ).save()
            new_choice2 = Choice(
                                    poll = new_poll,
                                    choice_text=form.cleaned_data['choice2']
                                ).save()
            messages.success(
                            request,
                            'Poll and Choices added!',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('polls:list')
    else:
        form = PollForm()
    context = {'form': form}
    return render(request, 'polls/add_poll.html', context)

@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('/')

    if request.method == "POST":
        poll.delete()
        messages.success(
                        request,
                        'Poll Deleted Successfully',
                        extra_tags='alert alert-success alert-dismissible fade show'
                        )
        return redirect('polls:list')

    return render(request, 'polls/delete_poll_confirm.html', {'poll':poll})

@login_required
def edit_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('/')

    if request.method == "POST":
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            messages.success(
                            request,
                            'Poll Edit Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('polls:list')
    else:
        form = EditPollForm(instance=poll)

    return render(request, 'polls/edit_poll.html', {'form': form, 'poll':poll})

@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.user != poll.owner:
        return redirect('/')

    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                            request,
                            'Choice Added Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('polls:list')
    else:
        form = ChoiceForm()
    return render(request, 'polls/add_choice.html', {'form':form})

@login_required
def edit_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)
    if request.user != poll.owner:
        return redirect('/')

    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            form.save()
            messages.success(
                            request,
                            'Choice Edited Successfully',
                            extra_tags='alert alert-success alert-dismissible fade show'
                            )
            return redirect('polls:list')
    else:
        form = ChoiceForm(instance=choice)
    return render(request, 'polls/add_choice.html', {'form':form, 'edit_mode': True, 'choice':choice})

@login_required
def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll = get_object_or_404(Poll, id=choice.poll.id)
    if request.user != poll.owner:
        return redirect('/')

    if request.method == "POST":
        choice.delete()
        messages.success(
                        request,
                        'Choice Deleted Successfully',
                        extra_tags='alert alert-success alert-dismissible fade show'
                        )
        return redirect('polls:list')

    return render(request, 'polls/delete_choice_confirm.html', {'choice':choice})

@login_required
def poll_detail(request, poll_id):
    """
    Render the poll_detail.html template which allows a user to vote
    on the choices of a poll
    """
    # poll = Poll.objects.get(id=poll_id)
    poll = get_object_or_404(Poll, id=poll_id)
    user_can_vote = poll.user_can_vote(request.user)
    results = poll.get_results_dict()
    context = {'poll': poll, 'user_can_vote': user_can_vote, 'results': results}
    return render(request, 'polls/poll_detail.html', context)

@login_required
def poll_vote(request, poll_id):
    # try:
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.user_can_vote(request.user):
        messages.error(request, 'Are you crazy? You have already voted on this poll!')
        return redirect('polls:detail', poll_id=poll_id)

    choice_id = request.POST.get('choice')
    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        new_vote = Vote(user=request.user, poll=poll, choice=choice)
        new_vote.save()
    else:
        messages.error(request, 'No Choice Was Found!')
        return redirect('polls:detail', poll_id=poll_id)
    return redirect('polls:detail', poll_id=poll_id)
