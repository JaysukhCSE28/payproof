"""Accuracy, planted-error recall, and decoy false-positive metrics."""

from backend.app.models import Verdict


def accuracy(predicted: list[Verdict], expected: list[Verdict]) -> float:
    # TODO: overall verdict accuracy
    raise NotImplementedError("accuracy")
