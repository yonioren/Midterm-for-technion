from flask import render_template
from . import statistics_bp
from ..models import inventory_items, projects

@statistics_bp.route('/')
def view_stats():
    total_price = []
    project_sizes = []

    for p in projects:
        cost = 0
        size = 0
        for item_id, qty in p.resources.items():
            item = next((i for i in inventory_items if i.id == item_id), None)
            if item:
                cost += item.price * qty
                size += qty
        total_price.append(cost)
        project_sizes.append((size, p))

    avg_price = sum(total_price) / len(total_price) if total_price else 0
    total_cost = sum(total_price)
    largest_project = max(project_sizes, default=(0, None))[1]

    return render_template(
        'statistics.html',
        avg_price=avg_price,
        total_price=total_cost,
        largest_project=largest_project
    )
