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
    most_expensive_project_cost = 0
    largest_project = None
    largest_project_resource_count = 0
    most_used_item = None
    most_used_count = 0
    avg_resources = 0
    cpu_count = 0
    ram_count = 0
    hd_sum = 0

    # Calculate project based statistics
    if projects:
        project_costs = []
        resource_counts = []
        usage_counter = {}

        for project in projects:
            total_cost = 0
            total_resources = 0
            ## Go over all items of the project and calculate
            for item_id, qty in project.resources.items():
                item = next((i for i in inventory_items if i.id == item_id), None)
                if item:
                    total_cost += item.price * qty
                    total_resources += qty
                    usage_counter[item_id] = usage_counter.get(item_id, 0) + qty
                    cpu_count+=item.cpu * qty
                    ram_count+=item.ram * qty
                    hd_sum+=item.hd * qty

            project_costs.append((project, total_cost))
            resource_counts.append((project, total_resources))

        # Calculate project statistics based on price
        if project_costs:
            for proj_tup in project_costs:
                total_sum += proj_tup[1]
                if most_expensive_project_cost <= proj_tup[1]:
                    most_expensive_project_cost = proj_tup[1]
                    most_expensive_project = proj_tup[0]
            avg_price = total_sum / len(project_costs)

        # Calculate project statistics based on content in project
        if resource_counts:
            for res_tup in resource_counts:
                if largest_project_resource_count <= res_tup[1]:
                    largest_project_resource_count = res_tup[1]
                    largest_project = res_tup[0]
            # largest_project = max(resource_counts, key=lambda x: x[1])[0]
            avg_resources = sum(c for _, c in resource_counts) / len(resource_counts)

        # Calculate project statistics based on inventory usage
        if usage_counter:
            most_used_item=0
            most_used_count=0
            most_used_item_id=0
            for k, v in usage_counter.items():
                if v > most_used_count:
                    most_used_count = v
                    most_used_item_id = k
            for item in inventory_items:
                if item.id == most_used_item_id:
                    most_used_item = item

    # I might consider creating a class to make it more readable one day
    return render_template(
        'statistics.html',
        avg_price=avg_price,
        total_sum=total_sum,
        cpu_count=cpu_count,
        ram_count=ram_count,
        hd_sum=hd_sum,
        project_count=project_count,
        inventory_count=inventory_count,
        most_expensive_project=most_expensive_project,
        most_expensive_project_cost=most_expensive_project_cost,
        largest_project=largest_project,
        largest_project_resource_count=largest_project_resource_count,
        most_used_item=most_used_item,
        most_used_count=most_used_count,
        avg_resources=avg_resources
    )
