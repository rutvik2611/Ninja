import os
import subprocess

from src.helper.helper import print_file_structure


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

def deploy_service(service_name):
    service_path = os.path.join(os.getcwd(), 'services', service_name)
    docker_compose_files = [f for f in os.listdir(service_path) if f.endswith(".yml") or f.endswith(".yaml")]

    if len(docker_compose_files) == 1:
        docker_compose_file = docker_compose_files[0]
        docker_compose_path = os.path.join(service_path, docker_compose_file)
        print(f"Deploying {docker_compose_file}...")
        subprocess.run(["docker-compose", "-f", docker_compose_path, "up", "-d"])
        print(f"{docker_compose_file} has been deployed.")
    elif docker_compose_files:
        print(f"Found multiple Docker Compose files in '{service_name}' folder. Please select a specific file or enter 'all' to deploy all files.")
        for index, file in enumerate(docker_compose_files):
            print(f"{index + 1}. {file}")

        file_choice = input("Select a Docker Compose file to deploy (enter the file number) or type 'all' to deploy all files or 'exit' to return to the main menu: ")
        if file_choice == 'exit':
            return

        if file_choice.lower() == 'all':
            for docker_compose_file in docker_compose_files:
                docker_compose_path = os.path.join(service_path, docker_compose_file)
                print(f"Deploying {docker_compose_file}...")
                subprocess.run(["docker-compose", "-f", docker_compose_path, "up", "-d"])
                print(f"{docker_compose_file} has been deployed.")
        elif file_choice.isdigit():
            file_choice = int(file_choice)
            if 1 <= file_choice <= len(docker_compose_files):
                docker_compose_file = docker_compose_files[file_choice - 1]
                docker_compose_path = os.path.join(service_path, docker_compose_file)
                print(f"Deploying {docker_compose_file}...")
                subprocess.run(["docker-compose", "-f", docker_compose_path, "up", "-d"])
                print(f"{docker_compose_file} has been deployed.")
            else:
                print("Invalid file number.")
        else:
            print("Please enter a valid number or 'all'.")
    else:
        print(f"No Docker Compose or YAML files found in '{service_name}' folder.")


if __name__ == '__main__':
    while True:
        print("Select an option:")
        print("1. Print File Structure")
        print("2. List Available Services")
        print("3. Exit")

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
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option (1, 2, or 3).")
