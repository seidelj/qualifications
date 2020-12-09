from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import boto3
from otree.views.mturk import get_mturk_client
import settings

class PaymentInfo(Page):

    def is_displayed(self):
        return self.participant.vars['passed_quiz']


    #self.participant.payoff_plus_participation_fee()
    def vars_for_template(self):
        return {
            'payoff': self.participant.payoff.to_real_world_currency(self.session)
        }

    def before_next_page(self):
        # assigns a qualification indicating that the worker has
        # completed the study.
        p = self.participant
        payoff = p.payoff_in_real_world_currency()
        # assign qualification
        if self.session.is_mturk:
            mturk_client = get_mturk_client(use_sandbox=self.session.mturk_use_sandbox)
            EDA1_SANDBOX = settings._AMK1_SANDBOX
            EDA1 = settings._AMK1
            qid = EDA1_SANDBOX if self.session.mturk_use_sandbox else EDA1
            mturk_client.associate_qualification_with_worker(
                QualificationTypeId=qid,
                WorkerId=p.mturk_worker_id,
                IntegerValue=1,
            )

class Incomplete(Page):

    def is_displayed(self):
        return self.participant.vars['passed_quiz'] == 0

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    PaymentInfo,
    Incomplete
]
