from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.views.mturk import get_mturk_client


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'qualification'
    players_per_group = None
    num_rounds = 1

    start_time = "3pm, EDT"
    use_sandbox = False


class Subsession(BaseSubsession):

    qualificationTypeId = models.CharField()

    def creating_session(self):
        if self.session.config['qualId'] == 'none':
            # create a qualification corresponding
            mturk_client = get_mturk_client(use_sandbox=Constants.use_sandbox) # this code is ran before mturk is
            response = mturk_client.create_qualification_type(
                Name='Qualification_{}'.format(self.session.code),
                Description='Qualification for workers to participate',
                QualificationTypeStatus='Active',
                AutoGranted=False,
            )
            self.qualificationTypeId = response['QualificationType']['QualificationTypeId']
        else:
            self.qualificationTypeId = self.session.config['qualId']

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    captcha = models.CharField(blank=True)
    question = models.BooleanField(
        choices = [
            [False, 'No, please do not invite me'],
            [True, 'Yes, I commit to showing up at {}'.format(Constants.start_time)],
        ],
        label="Would you like to participate and can you commit to joining the study?",
    )

    consent = models.BooleanField(
        choices = [
            [False, 'No, I don\'t wish to participate.'],
            [True, 'Yes, I have read and agree to the above study information.'],
        ],
        label="Please indicate that you've read and agree to participate in this study."
    )

    mturkId = models.CharField()

    def set_mturkId(self):
        self.mturkId = self.participant.mturk_worker_id
