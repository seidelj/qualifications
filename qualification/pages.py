from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree.views.mturk import get_mturk_client
from callmkts.models import Constants as CM_Constants
from captcha.fields import ReCaptchaField

class Qualification(Page):

    form_model = 'player'
    form_fields = ['question', 'captcha']

    def vars_for_template(self):
        todOrTom = self.session.config['todOrTom']
        month = self.session.config['month']
        day = self.session.config['day']
        time = Constants.start_time
        date_str = '{}, {} {} at {}'.format(todOrTom, month, day, time)
        return {
            'todOrTom': todOrTom,
            'DA_Constants': CM_Constants,
            'date_str': date_str,
        }


    def get_form(self, data=None, files=None, **kwargs):
        frm = super().get_form(data, files, **kwargs)
        frm.fields['captcha'] = ReCaptchaField(label='')
        return frm

    def before_next_page(self):
        self.player.set_mturkId()
        # assign qualification
        mturk_client = get_mturk_client(use_sandbox=self.session.mturk_use_sandbox)
        if self.player.question == True:
            mturk_client.associate_qualification_with_worker(
                QualificationTypeId=self.subsession.qualificationTypeId,
                WorkerId=self.player.participant.mturk_worker_id,
                IntegerValue=1,
            )

class SIS(Page):

    def is_displayed(self):
        return self.player.question == 1

    form_model = 'player'
    form_fields = ['consent']

    def before_next_page(self):
        if self.player.consent == False and self.player.question == True:
            mturk_client = get_mturk_client(use_sandbox=self.session.mturk_use_sandbox)
            mturk_client.disassociate_qualification_from_worker(
                QualificationTypeId=self.subsession.qualificationTypeId,
                WorkerId=self.player.participant.mturk_worker_id,
                Reason='No consent'
            )

class Results(Page):

    def vars_for_template(self):
        todOrTom = self.session.config['todOrTom']
        month = self.session.config['month']
        day = self.session.config['day']
        time = Constants.start_time
        date_str = '{}, {} {} at {}.'.format(todOrTom.lower(), month, day, time)
        return { 'date_str': date_str }



page_sequence = [
    Qualification,
    SIS,
    Results
]
