# make sure to install faker...
# pip install faker
import datetime
import random
from faker import Faker
fake = Faker()

from django.contrib.auth.models import User
from polls.models import Choice, Poll, Vote

def seed_users(num_entries=10, overwrite=False):
    """
    Creates num_entries worth a new users
    """
    if overwrite:
        print("Overwriting Users")
        Users.objects.all().delete()
    count = 0
    for _ in range(num_entries):
        first_name = fake.first_name()
        last_name = fake.last_name()
        u = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            email = first_name + "." + last_name + "@fakermail.com",
            username = first_name + last_name,
            password="password"
        )
        count += 1
    print("Created {} new users".format(count))

def seed_polls(num_entries=10, choice_min=2, choice_max=5, overwrite=False):
    """
    Seeds num_entries poll with random users as owners
    Each poll will be seeded with # choices from choice_min to choice_max
    """
    if overwrite:
        print('Overwriting polls')
        Poll.objects.all().delete()
    users = list(User.objects.all())
    count = 0
    for _ in range(num_entries):
        p = Poll(
            owner = random.choice(users),
            text = fake.paragraph(),
            pub_date = datetime.datetime.now()
        )
        p.save()
        for _ in range(choice_min, choice_max + 1):
            c = Choice(
                poll = p,
                choice_text = fake.sentence()
            ).save()
        count += 1
    print("Created {} new polls".format(count))

def seed_votes(overwrite=True):
    """
    Creates a new vote on every poll for every user
    Voted for choice is selected random.
    Deletes all votes prior to adding new ones
    """
    Vote.objects.all().delete()
    users = User.objects.all()
    polls = Poll.objects.all()
    for poll in polls:
        for user in users:
            choices = list(poll.choice_set.all())
            v = Vote(
                user = user,
                poll = poll,
                choice = random.choice(choices)
            ).save()

def seed_all(overwrite=False):
    """
    Runs all seeder functions. Passes value of overwrite to all
    seeder function calls.
    """
    seed_users(overwrite=overwrite)
    seed_polls(overwrite=overwrite)
    seed_votes(overwrite=overwrite)
