with open('main.py', 'r') as file:
    lines = file.readlines()
    code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
    print(len(code_lines))