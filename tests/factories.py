from datetime import datetime

import factory

from server.apps.main.models import Poll, Question


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    type = "ONE"
    description = "Description"
    variants = ["some correct", "some incorrect", "some statement"]
    answers = ["correct", "-", "-"]


class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Poll

    name = "Poll name"
    description = "Poll description"
    start_date = datetime(1970, 1, 1, 1, 1, 1)
    end_date = datetime(2070, 1, 1, 1, 1, 1)

    @factory.post_generation
    def questions(self, create, extracted, **kwargs):

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.questions.add(group)
