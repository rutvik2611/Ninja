import os

from src.old.helper.helper import deploy_service, build_and_deploy_jenkins


def print_file_structure(root_directory, indent=""):
    """
    Recursively prints the complete file structure starting from the given directory.

    :param root_directory: The directory to start printing the file structure from.
    :param indent: A string used for indentation to represent the directory hierarchy.
    """
    items = os.listdir(root_directory)
    num_items = len(items)

    ignore_list = ['.idea', 'node_modules','jenkins-volume','__pycache__','Pipfile.lock','output_directory']

    for index, item in enumerate(items):
        item_path = os.path.join(root_directory, item)
        is_last = index == num_items - 1
        if item not in ignore_list:
            print(f"{indent}{'└─' if is_last else '├─'} {item}")

            if os.path.isdir(item_path):
                next_indent = indent + ("    " if is_last else "│   ")
                print_file_structure(item_path, next_indent)
def print_file_structure_and_content(root_directory, indent=""):
    """
    Recursively prints the file structure starting from the given directory and
    displays the contents of the files.

    :param root_directory: The directory to start printing the file structure from.
    :param indent: A string used for indentation to represent the directory hierarchy.
    """
    items = os.listdir(root_directory)
    num_items = len(items)

    ignore_list = ['.idea', 'node_modules', 'jenkins-volume', '__pycache__', 'Pipfile.lock', 'output_directory']

    for index, item in enumerate(items):
        item_path = os.path.join(root_directory, item)
        is_last = index == num_items - 1

        # Check if the current item should be ignored
        if item in ignore_list:
            continue

        # Print the current item's name
        print(f"{indent}{'└─' if is_last else '├─'} {item}")

        if os.path.isdir(item_path):
            # If the current item is a directory, recursively call the function
            next_indent = indent + ("    " if is_last else "│   ")
            print_file_structure_and_content(item_path, next_indent)
        else:
            # If the current item is a file, display its contents
            try:
                with open(item_path, 'r') as file_content:
                    print(f"{indent}  {'└─' if is_last else '├─'} [Contents of {item}]:")
                    # Reading the content of the file
                    contents = file_content.read()
                    # Printing the content of the file with additional indentation
                    for line in contents.split('\n'):
                        print(f"{indent}  {'    ' if is_last else '│   '}{line}")
            except Exception as e:
                # If the file cannot be read, display an error message
                print(f"{indent}  {'└─' if is_last else '├─'} [Error reading {item}]: {e}")
def list_available_services():
    services_directory = os.path.join(os.getcwd(), 'services')
    services = [service for service in os.listdir(services_directory) if os.path.isdir(os.path.join(services_directory, service))]
    print("Available services:")
    for index, service in enumerate(services):
        print(f"{index + 1}. {service}")

    while True:
        service_choice = input("Select a service to deploy (enter the service number) or type 'exit' to return to the main menu: ")
        if service_choice == 'exit':
            break
        if service_choice.isdigit():
            service_choice = int(service_choice)
            if 1 <= service_choice <= len(services):
                deploy_service(services[service_choice - 1])
                deploy_another = input("Deploy another service? (yes/no): ")
                if deploy_another.lower() != 'yes':
                    break
            else:
                print("Invalid service number.")
        else:
            print("Please enter a valid number.")




if __name__ == '__main__':
    while True:
        print("\nSelect an option:")
        print("1. Print File Structure")
        print("2. List Available Services")
        print("3. Build Jenkins")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            directory_path = os.getcwd()
            if os.path.exists(directory_path):
                print(f"File structure starting from: {directory_path}")
                print_file_structure(directory_path)

            else:
                print(f"The directory '{directory_path}' does not exist.")
        elif choice == '2':
            list_available_services()
        elif choice == '3':
            build_and_deploy_jenkins()
        elif choice == '4':
            # directory_path = os.getcwd()
            # print_file_structure_and_content(directory_path)
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
