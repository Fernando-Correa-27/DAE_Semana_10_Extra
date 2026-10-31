"""Seed command to load the 6 plans from Phase A's plans.js.

Usage:  python manage.py seed_plans
"""

import json
from typing import Any

from django.core.management.base import BaseCommand

from plans.seeds import PLANS


class Command(BaseCommand):
    help = "Seed the database with the 6 plans from Phase A."

    def handle(self, *args: Any, **options: Any) -> None:
        from plans.models import Plan
        from plans.services import compute_plan_hash

        created = 0
        updated = 0

        for plan_data in PLANS:
            target = plan_data["target"]
            op = plan_data["op"]

            # Compute path_args per the same logic as the frontend
            if "destroy" in op:
                path_args = {"id": target.get("id")}
            else:
                path_args = {}

            plan_hash = compute_plan_hash(op, path_args, target)

            plan, created_plan = Plan.objects.update_or_create(
                id_plan=plan_data["id_plan"],
                defaults={
                    "op": plan_data["op"],
                    "risk": plan_data["risk"],
                    "target": target,
                    "proposed_by": plan_data["proposed_by"],
                    "plan_hash": plan_hash,
                },
            )

            if created_plan:
                created += 1
            else:
                updated += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created_plan else 'Updated'} {plan.id_plan} "
                    f"– hash: {plan.plan_hash}"
                )
            )

        total = created + updated
        self.stdout.write(
            self.style.SUCCESS(f"Total plans processed: {total} (created: {created}, updated: {updated})")
        )
