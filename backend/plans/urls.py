"""URL configuration for the plans app."""

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PlanViewSet, PlanDecisionView

router = DefaultRouter()
router.register(r"plans", PlanViewSet, basename="plan")

# Decision endpoint
decision_patterns = [
    path(
        "plans/<str:id_plan>/decision/",
        PlanDecisionView.as_view({"post": "create"}),
        name="plan-decision",
    ),
]

urlpatterns = router.urls + decision_patterns
