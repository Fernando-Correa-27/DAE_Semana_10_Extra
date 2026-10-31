"""Django model for a proposed plan."""

from django.db import models


class Plan(models.Model):
    """A plan proposal that the approval board may approve or reject."""

    id_plan = models.CharField(max_length=10, primary_key=True)
    op = models.CharField(max_length=64)
    risk = models.CharField(max_length=4)
    target = models.JSONField()
    proposed_by = models.CharField(max_length=64)
    plan_hash = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "plans_plan"
        ordering = ["id_plan"]

    def __str__(self):
        return f"{self.id_plan} – {self.op} ({self.risk})"
