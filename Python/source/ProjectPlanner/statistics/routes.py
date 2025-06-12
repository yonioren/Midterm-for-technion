from flask import render_template
from . import statistics_bp
from ..models import inventory_items, projects

@statistics_bp.route('/')
def show_stats():
    # Defaults
    avg_price = 0
    total_sum = 0
    project_count = len(projects)
    inventory_count = len(inventory_items)
    most_expensive_project = None
    largest_project = None
    most_used_item = None
    most_used_count = 0
    avg_resources = 0

    if projects:
        project_costs = []
        resource_counts = []
        usage_counter = {}

        for project in projects:
            total_cost = 0
            total_resources = 0
            for item_id, qty in project.resources.items():
                item = next((i for i in inventory_items if i.id == item_id), None)
                if item:
                    total_cost += item.price * qty
                    total_resources += qty
                    usage_counter[item_id] = usage_counter.get(item_id, 0) + qty

            project_costs.append((project, total_cost))
            resource_counts.append((project, total_resources))

        if project_costs:
            total_sum = sum(cost for _, cost in project_costs)
            avg_price = total_sum / len(project_costs)
            most_expensive_project = max(project_costs, key=lambda x: x[1])[0]

        if resource_counts:
            largest_project = max(resource_counts, key=lambda x: x[1])[0]
            avg_resources = sum(c for _, c in resource_counts) / len(resource_counts)

        if usage_counter:
            most_used_item_id = max(usage_counter, key=usage_counter.get)
            most_used_item = next((i for i in inventory_items if i.id == most_used_item_id), None)
            most_used_count = usage_counter[most_used_item_id]

    return render_template(
        'statistics.html',
        avg_price=avg_price,
        total_sum=total_sum,
        project_count=project_count,
        inventory_count=inventory_count,
        most_expensive_project=most_expensive_project,
        largest_project=largest_project,
        most_used_item=most_used_item,
        most_used_count=most_used_count,
        avg_resources=avg_resources
    )
