from django.contrib.auth.models import User

from factories import *


def test_get_polls(client) -> None:
    """This test ensures that getting polls works."""
    p1 = PollFactory(
        questions=[QuestionFactory(), QuestionFactory(), QuestionFactory()]
    )
    p2 = PollFactory(
        questions=[QuestionFactory(), QuestionFactory(), QuestionFactory()]
    )
    response = client.get("/active_polls")
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == p1.name and data[1]["name"] == p2.name


def test_create_poll(client) -> None:
    """This test ensures that poll can be created"""

    request = {
        "name": "new_poll",
        "description": "new_description",
        "start_date": "1970-01-01T01:01:01Z",
        "end_date": "2025-01-01T01:01:01Z",
    }
    response = client.post("/polls/", data=request, format="json")
    assert response.status_code == 201

    request["start_date"] = request["end_date"]
    response = client.post("/polls/", data=request, format="json")
    assert response.status_code == 400


def test_update_poll(client) -> None:
    p1 = PollFactory()
    response = client.patch(
        f"/polls/{p1.id}/", data={"name": "changed name"}, format="json"
    )
    assert response.status_code == 200
    assert Poll.objects.filter(id=p1.id)[0].name == "changed name"


def test_delete_poll(client) -> None:
    p1 = PollFactory()
    PollFactory(), PollFactory()
    client.delete(f"/polls/{p1.id}/")
    assert Poll.objects.all().count() == 2


def test_create_question(client) -> None:
    p1 = PollFactory()
    assert p1.questions.count() == 0
    question = {
        "description": "Capital of England2222",
        "type": "MULTIPLE",
        "variants": ["Moscow", "London", "Londondon"],
        "answers": ["-", "correct", "correct"],
        "poll_id": p1.id,
    }
    response = client.post("/questions/", data=question, format="json")

    p1.refresh_from_db()
    assert response.status_code == 201
    assert p1.questions.count() == 1

    response = client.post("/questions/", data=question, format="json")

    p1.refresh_from_db()
    assert response.status_code == 201
    assert p1.questions.count() == 2


def test_update_question(client) -> None:
    q1 = QuestionFactory()
    # two correct answers for question of type of 'one correct answer'
    response = client.patch(
        f"/questions/{q1.id}/", data={"answers": ["correct, correct"]}, format="json"
    )
    assert response.status_code == 400
    assert q1.type == "ONE"

    response = client.patch(
        f"/questions/{q1.id}/",
        data={"type": "TEXT", "variants": ["v1"], "answers": ["answer"]},
        format="json",
    )
    assert response.status_code == 200

    response = client.patch(
        f"/questions/{q1.id}/",
        data={
            "type": "MULTIPLE",
            "variants": ["v1", "v2"],
            "answers": ["correct", "correct"],
        },
        format="json",
    )
    q1.refresh_from_db()
    assert response.status_code == 200 and q1.type == "MULTIPLE"


def test_delete_question(client) -> None:
    q1 = QuestionFactory()
    response = client.delete(f"/questions/{q1.id}/")
    assert response.status_code == 204
    assert Question.objects.count() == 0


def test_no_pass_poll(client) -> None:
    q1 = QuestionFactory(type="ONE", answers=["correct", "-", "-"])
    q2 = QuestionFactory(
        type="TEXT",
        answers=[
            "answers",
        ],
    )
    q3 = QuestionFactory(type="Multiple", answers=["correct", "-", "correct"])
    p1 = PollFactory(questions=[q1, q2, q3])
    response = client.post(
        "/pass_poll",
        data={
            "user_id": 5,
            "poll_id": p1.id,
            "answers": [
                ["-", "-", "-"], # no answer provided for this question
                ["answer"],
                ["correct", "correct", "-"],
            ],
        },
    )
    assert response.status_code == 400
