from pyslvs import example_list, parse_vpoints, t_config, expr_solving

# Get example with name
expr, inputs = example_list("Jansen's linkage (Single)")
# Parse the mechanism expression into a list of joint data
vpoints = parse_vpoints(expr)
# Config joint data and control data for the solver
exprs = t_config(vpoints, inputs)
# Solve the position
result = expr_solving(exprs, vpoints, {pair: 0. for pair in inputs})
# Get the result from joint 7
x, y = result[7]
print(x, y)  # -43.170055 -91.753226
