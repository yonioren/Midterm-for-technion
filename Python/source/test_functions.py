import pytest
from ProjectPlanner.controllers.inventory import list_inventory_items
from ProjectPlanner.controllers.projects import list_projects

def test_list_inventory_items_check_dummy_data_on_first_run():
    length_of_dummy = 3

    assert len(list_inventory_items()) == length_of_dummy

def test_list_projects_check_dummy_data_on_first_run():
    length_of_dummy = 1

    projects, _ = list_projects()
    assert len(projects) == length_of_dummy
