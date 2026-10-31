"""Views for the plans API."""

from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Plan
from .serializers import PlanSerializer, DecisionSerializer
from .services import compute_plan_hash


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """List all plans.  plan_hash is recomputed on the server for every plan."""

    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]


class PlanDecisionView(viewsets.ViewSet):
    """Accept a decision (approve/reject) for a single plan.

    POST /api/plans/<id_plan>/decision/
    """

    permission_classes = [permissions.AllowAny]

    def create(self, request, id_plan=None):
        """Handle the decision endpoint for a plan."""
        serializer = DecisionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verdict = serializer.validated_data["verdict"]
        typed_hash = serializer.validated_data["typed_hash"]

        try:
            plan = Plan.objects.get(id_plan=id_plan)
        except Plan.DoesNotExist:
            return Response(
                {"error": _("Plan no encontrado.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        if verdict == DecisionSerializer.VERDICT_APPROVE:
            # R2: approved only if typed_hash is an exact match
            if not plan.plan_hash or not typed_hash:
                return Response(
                    {"error": _("Falta el hash o el typed_hash.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Use constant-time comparison to prevent timing attacks
            if not __import__("hmac", fromlist=["compare_digest"]).compare_digest(
                plan.plan_hash, typed_hash
            ):
                return Response(
                    {
                        "error": _(
                            "El typed_hash no coincide con el plan_hash "
                            "del plan. No se puede aprobar."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            return Response(
                {
                    "message": _("Plan aprobado correctamente."),
                    "plan": PlanSerializer(plan).data,
                },
                status=status.HTTP_200_OK,
            )

        # Reject is always valid
        return Response(
            {"message": _("Plan rechazado."), "plan": PlanSerializer(plan).data},
            status=status.HTTP_200_OK,
        )
