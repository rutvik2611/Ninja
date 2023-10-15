import os


def print_file_structure(root_directory, indent=""):
    """
    Recursively prints the complete file structure starting from the given directory.

    :param root_directory: The directory to start printing the file structure from.
    :param indent: A string used for indentation to represent the directory hierarchy.
    """
    items = os.listdir(root_directory)
    num_items = len(items)

    ignore_list = ['.idea', 'node_modules','jenkins-volume','__pycache__']

    for index, item in enumerate(items):
        item_path = os.path.join(root_directory, item)
        is_last = index == num_items - 1
        if item not in ignore_list:
            print(f"{indent}{'└─' if is_last else '├─'} {item}")

            if os.path.isdir(item_path):
                next_indent = indent + ("    " if is_last else "│   ")
                print_file_structure(item_path, next_indent)