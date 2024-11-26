from scipy.optimize import linprog
# from model import models
import streamlit as st


@st.cache_data
def allocate_employees_to_projects(projects, categories):

    # Sort projects by descending hours for prioritization
    sorted_projects = sorted(projects.items(), key=lambda x: x[1], reverse=True)

    # Extract category details
    category_names = list(categories.keys())
    available_employees = {k: v[0] for k, v in categories.items()}  # Available employee counts
    billable_hours = {k: v[1] for k, v in categories.items()}  # Hours worked per employee per category

    num_categories = len(category_names)
    allocations = {}  # To store allocation results for each project

    for proj_name, proj_hours in sorted_projects:
        # Prepare inputs for linear programming
        category_hours = [billable_hours[cat] for cat in category_names]
        bounds = [(0, available_employees[cat]) for cat in category_names]
        c = [1] * num_categories  # Objective: Minimize total employees used

        A_eq = [[category_hours[j] for j in range(num_categories)]]
        b_eq = [proj_hours]

        # Solve the linear programming problem
        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        if result.success:
            # Convert the solution to integer values
            employees_needed = {category_names[i]: max(0, round(result.x[i])) for i in range(num_categories)}
            allocations[proj_name] = employees_needed

            # Update available employees
            for category, assigned in employees_needed.items():
                available_employees[category] -= assigned
        else:
            raise ValueError(f"Optimization failed for project {proj_name}: {result.message}")

    return allocations, available_employees