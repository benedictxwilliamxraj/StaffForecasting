from scipy.optimize import linprog

def allocate_employees(project_hours, categories, max_employees):
    # Extract category details
    category_names = list(categories.keys())
    category_hours = list(categories.values())
    num_categories = len(category_names)


    for i in range(num_categories):
        if category_hours[i] == 0:
            category_hours[i] = 1

    # Objective function: Minimize the total number of employees used
    c = [1] * num_categories  # Coefficients for minimizing total employees


    A_eq = [[category_hours[j] for j in range(num_categories)]]
    b_eq = [project_hours]

    # Bounds: Employees per category cannot exceed the max available
    bounds = [(0, max_employees[category_names[i]]) for i in range(num_categories)]

    # Fairness constraints: Relaxed fairness factor
    fairness_factor = 3  # Relaxed fairness factor
    A_ub = []
    b_ub = []
    for i in range(num_categories):
        for j in range(i + 1, num_categories):
            row = [0] * num_categories
            row[i] = 1
            row[j] = -fairness_factor
            A_ub.append(row)
            b_ub.append(0)

    # Solve the linear programming problem
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

    if result.success:
        # Convert the solution to integer values
        employees_needed = {category_names[i]: max(0, round(result.x[i])) for i in range(num_categories)}
        return employees_needed
    else:
        raise ValueError(f"Optimization failed: {result.message}")
