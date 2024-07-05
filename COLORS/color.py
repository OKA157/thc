def print_colored_text(text, color):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_purple': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'orange': '\033[38;5;208m',
        'reset': '\033[0m',
    }

    if color not in colors:
        print("Invalid color. Please choose from: black, red, green, yellow, blue, purple, cyan, white, bright_black, bright_red, bright_green, bright_yellow, bright_blue, bright_purple, bright_cyan, bright_white, orange")
        return

    colored_text = f"{colors[color]}{text}{colors['reset']}"
    print(colored_text, end='')
