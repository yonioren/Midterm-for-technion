from flask import render_template
from . import statistics_bp
from ..controllers.statistics import get_stats

@statistics_bp.route('/')
def show_stats():
    stats = get_stats()
    return render_template('statistics.html',
                           avg_price=stats['avg_price'],
                           total_sum=stats['total_sum'],
                           cpu_count=stats['cpu_count'],
                           ram_count=stats['ram_count'],
                           hd_sum=stats['hd_sum'],
                           project_count=stats['project_count'],
                           inventory_count=stats['inventory_count'],
                           most_expensive_project=stats['most_expensive_project'],
                           most_expensive_project_cost=stats['most_expensive_project_cost'],
                           largest_project=stats['largest_project'],
                           largest_project_resource_count=stats['largest_project_resource_count'],
                           most_used_item=stats['most_used_item'],
                           most_used_count=stats['most_used_count'],
                           avg_resources=stats['avg_resources']
    )
