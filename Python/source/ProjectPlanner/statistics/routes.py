from flask import render_template
from . import statistics_bp
from ..models import inventory_items, projects

@statistics_bp.route('/')
def view_stats():
    total_price = []
    project_sizes = []
    most_expensive = (0, None)
    resource_usage = {}

    for p in projects:
        cost = 0
        size = 0
        for item_id, qty in p.resources.items():
            item = next((i for i in inventory_items if i.id == item_id), None)
            if item:
                cost += item.price * qty
                size += qty
                resource_usage[item_id] = resource_usage.get(item_id, 0) + qty
        total_price.append(cost)
        project_sizes.append((size, p))
        if cost > most_expensive[0]:
            most_expensive = (cost, p)

    avg_price = sum(total_price) / len(total_price) if total_price else 0
    total_cost = sum(total_price)
    largest_project = max(project_sizes, default=(0, None))[1]
    most_expensive_project = most_expensive[1]

    if resource_usage:
        most_used_id = max(resource_usage.items(), key=lambda x: x[1])[0]
        most_used_item = next((i for i in inventory_items if i.id == most_used_id), None)
        most_used_count = resource_usage[most_used_id]
    else:
        most_used_item = None
        most_used_count = 0

    avg_resources = sum([sum(p.resources.values()) for p in projects]) / len(projects) if projects else 0

    return render_template(
        'statistics.html',
        avg_price=avg_price,
        total_price=total_cost,
        largest_project=largest_project,
        most_expensive_project=most_expensive_project,
        inventory_count=len(inventory_items),
        project_count=len(projects),
        most_used_item=most_used_item,
        most_used_count=most_used_count,
        avg_resources=avg_resources
    )
