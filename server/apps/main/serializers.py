from rest_framework import serializers

from server.apps.main.models import Question, Poll, PassedPoll, History


class UserQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "description", "type", "variants"]

    id = serializers.IntegerField(required=False)
    description = serializers.CharField()
    type = serializers.CharField()
    variants = serializers.ListField(child=serializers.CharField())


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ["id", "name", "description", "start_date", "end_date", "questions"]

    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    description = serializers.CharField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    questions = UserQuestionSerializer(many=True, read_only=True)


class AdminQuestionSerializer(UserQuestionSerializer):
    class Meta:
        model = Question
        fields = UserQuestionSerializer.Meta.fields + ["answers", "poll_id"]

    answers = serializers.ListField(child=serializers.CharField())
    poll_id = serializers.IntegerField(write_only=True)  # for which to create

    def validate(self, attrs):
        if "poll_id" in attrs and not Poll.objects.filter(pk=attrs["poll_id"]).exists():
            raise serializers.ValidationError("Wrong question data provided")

        n_variants = (
            len(attrs["variants"])
            if "variants" in attrs
            else len(self.instance.variants)
        )
        answs = attrs["answers"] if "answers" in attrs else self.instance.answers
        n_answers = len(answs)
        n_correct = len([x for x in answs if x != "-"])

        type = attrs["type"] if "type" in attrs else self.instance.type

        if (
            (n_variants != n_answers)
            or (type == "ONE" and n_correct != 1)
            or (type == "MULTIPLE" and n_correct <= 1)
            or (type == "TEXT" and n_answers != 1)
        ):  # or (type != "ONE" and type != "MULTIPLE" and type != "text"):
            raise serializers.ValidationError("Wrong question data provided")
        return attrs

    def create(self, validated_data):
        pk = validated_data.pop("poll_id")
        poll = Poll.objects.get(id=pk)
        question = Question.objects.create(**validated_data)
        poll.questions.add(question)
        poll.save()
        return question


class AdminPollSerializer(PollSerializer):
    questions = AdminQuestionSerializer(many=True, read_only=True)

    def validate(self, attrs):
        end_date = attrs["end_date"] if "end_date" in attrs else self.instance.end_date
        start_date = (
            attrs["start_date"] if "start_date" in attrs else self.instance.start_date
        )
        if end_date <= start_date:
            raise serializers.ValidationError("Wrong date")
        return attrs

    def create(self, validated_data):
        new_poll = Poll.objects.create(**validated_data)
        return new_poll


class PassedPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassedPoll
        fields = ["poll_id", "answers", "user_id"]

    user_id = serializers.IntegerField(write_only=True)
    poll_id = serializers.IntegerField()
    answers = serializers.ListField()

    def validate(self, attrs):
        poll = Poll.objects.get(id=attrs["poll_id"])
        for id, question in enumerate(poll.questions.all()):
            nansw = attrs["answers"][id]
            ncount = len([i for i in nansw[id] if i != "-"])
            if (
                (len(nansw) != len(question.variants))
                or ((question.type == "ONE" or question.type == "TEXT") and ncount != 1)
                or (question.type == "MULTIPLE" and ncount <= 1)
            ):
                raise serializers.ValidationError(
                    "Wrong answer format for some questions"
                )
        return attrs

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        passed_poll = PassedPoll(**validated_data)
        hist = History.objects.get_or_create(user_id=user_id)[0]
        hist.passes.add(passed_poll)
        hist.save()
        return passed_poll
