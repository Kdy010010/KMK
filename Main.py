def execute_line_fixed(line, variables):
    line = line.replace(";", "")

    if line.startswith("var"):
        var_name, value = line[4:].split("=")
        var_name = var_name.strip()
        value = eval(value.strip(), {}, variables)
        variables[var_name] = value

    elif line.startswith("print"):
        value = line[line.find("(")+1:line.find(")")]
        print(eval(value, {}, variables))

    elif line.startswith("for"):
        header, block = line.split("{")
        _, var_name, in_range = header.split()
        start, end = eval(in_range.strip(), {}, variables)
        block = block.rstrip("}")
        for i in range(start, end):
            variables[var_name] = i
            execute_line_fixed(block, variables)

    elif line.startswith("if"):
        condition, block = line.split("{")
        condition = condition[3:].strip()
        block = block.rstrip("}")
        if eval(condition, {}, variables):
            execute_line_fixed(block, variables)

    return variables

def execute_kmk_fixed(file_path):
    variables = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # First, execute import statements
    for line in lines:
        line = line.strip()
        if line.startswith("import") or line.startswith("from"):
            exec(line, variables)

    # Then execute the rest of the script
    for line in lines:
        line = line.strip()
        if not (line.startswith("import") or line.startswith("from")):
            if line:
                variables = execute_line_fixed(line, variables)
