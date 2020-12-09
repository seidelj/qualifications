from django.core.management.base import BaseCommand, CommandError
import csv
import sys
from django.apps import apps
from otree.models import Session
from qualification.models import Player, Constants, Subsession
#from double_auction.models import Subsession
import numpy as np
import pandas as pd
import settings
from otree.views.mturk import get_mturk_client


def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n:
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')

    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

#python manage.py model2csv --session wc1ybakl #use the qualification session.
class Command(BaseCommand):
    help = ("This command sends a reminder message to all Mturk workers who have the qualificationTypeId specified in SESSION_CONFIG_DEFAULTS")
    #args = '[appname.ModelName]'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--session', type=str, help='Provide session code', )

    def handle(self, *args, **kwargs):
        sessionCode = kwargs['session']
        if not confirm(prompt="Did you update the qualification?", resp=False):
            return
        model = apps.get_model('qualification', 'Player')
        qualificationTypeId = settings.SESSION_CONFIG_DEFAULTS['mturk_hit_settings']['qualification_requirements'][0]['QualificationTypeId']
        players = model.objects.filter(session__code=sessionCode).filter(question=True)
        print(players)
        workerIds = [ p.participant.mturk_worker_id for p in players ]
        session = Subsession.objects.filter(session__code=sessionCode)[0].session
        mturk_client = get_mturk_client(use_sandbox = session.mturk_use_sandbox)
        mturk_client.notify_workers(
            Subject='mturk Group Study Reminder',
            MessageText='This is a reminder that you agreed to participate in a group study today at: {}.  We will send you link when the HIT is posted.'.format(Constants.start_time),
            WorkerIds=workerIds
        )
