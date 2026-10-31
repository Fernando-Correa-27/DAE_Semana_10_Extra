"""Serializers for the plans app."""

from rest_framework import serializers

from .models import Plan
from .services import compute_plan_hash


class PlanSerializer(serializers.ModelSerializer):
    """Serialize a Plan, computing plan_hash on the server side."""

    class Meta:
        model = Plan
        fields = [
            "id_plan",
            "op",
            "risk",
            "target",
            "proposed_by",
            "plan_hash",
            "created_at",
        ]
        read_only_fields = ["plan_hash", "created_at"]

    def validate(self, attrs):
        """Recompute plan_hash from op, path_args, and target."""
        op = attrs.get("op", self.instance.op if self.instance else "")
        target = attrs.get("target", self.instance.target if self.instance else {})
        risk = attrs.get("risk", self.instance.risk if self.instance else "")

        # Determine path_args based on op
        if "destroy" in op:
            path_args = {"id": target.get("id")}
        else:
            path_args = {}

        computed = compute_plan_hash(op, path_args, target)
        attrs["plan_hash"] = computed
        return attrs


class DecisionSerializer(serializers.Serializer):
    """Input for the decision endpoint."""

    VERDICT_APPROVE = "approve"
    VERDICT_REJECT = "reject"

    verdict = serializers.ChoiceField(
        choices=[VERDICT_APPROVE, VERDICT_REJECT]
    )
    typed_hash = serializers.CharField(max_length=20)
