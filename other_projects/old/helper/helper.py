import os
import subprocess
import yaml


def build_and_deploy_jenkins():
    print("Building and deploying Jenkins service...")
    dockerfile_dir = os.path.join(os.getcwd(), 'services', 'jenkins')
    compose_file_path = os.path.join(dockerfile_dir, 'docker-compose-jenkins.yml')

    # Build the Docker image
    try:
        print("Building the Jenkins Docker image...")
        subprocess.run(["docker", "build", "-t", "my-custom-jenkins", dockerfile_dir], check=True)

        print("Constructing the docker run command from the compose file...")
        docker_run_command = docker_compose_to_run(compose_file_path)

        print("Running the Jenkins container...")
        subprocess.run(docker_run_command, check=True)
        print("Jenkins has been deployed. Access it at http://localhost:8080")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

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

def docker_compose_to_run(compose_file):
    """
    Translates a docker-compose.yml file into a docker run command.

    :param compose_file: Path to the docker-compose.yml file.
    :return: A docker run command as a list that can be passed to subprocess.run.
    """
    with open(compose_file, 'r') as file:
        compose_dict = yaml.safe_load(file)

    # We assume there's only one service in the docker-compose file for this example
    service_name, service_data = next(iter(compose_dict['services'].items()))
    image_name = service_data['image']

    command = ["docker", "run", "-d"]

    # Translate port mappings
    if 'ports' in service_data:
        for port in service_data['ports']:
            command.extend(["-p", port])

    # Translate volume mappings
    if 'volumes' in service_data:
        for volume in service_data['volumes']:
            command.extend(["-v", volume])

    # Translate environment variables
    if 'environment' in service_data:
        for env_var in service_data['environment']:
            command.extend(["-e", env_var])

    # Handle network settings
    network_name = None
    if 'networks' in service_data:
        # If there are specific network settings per service, we consider the first network
        network_name = next(iter(service_data['networks']))
    elif 'networks' in compose_dict:
        # Global networks for all services; consider the first one
        network_name = next(iter(compose_dict['networks']))

    if network_name:
        network_settings = compose_dict['networks'][network_name]
        if 'external' in network_settings and network_settings['external']:
            # For external networks, just connect to the existing network
            command.extend(["--network", network_name])
        else:
            # For internal or other custom networks, create the network (ignoring if it already exists)
            # and connect the container to it
            try:
                subprocess.run(["docker", "network", "create", network_name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                # Assuming the network is already created, else handle the exception accordingly
                pass
            command.extend(["--network", network_name])

    command.append(image_name)

    return command

def build_and_deploy_jenkins():
    print("Building and deploying Jenkins service...")
    dockerfile_dir = os.path.join(os.getcwd(), 'services', 'jenkins')
    compose_file_path = os.path.join(dockerfile_dir, 'docker-compose-jenkins.yml')

    # Build the Docker image
    try:
        print("Only Building the Jenkins Docker image...")
        subprocess.run(["docker", "build", "-t", "my-custom-jenkins", dockerfile_dir], check=True)

        # print("Constructing the docker run command from the compose file...")
        # docker_run_command = docker_compose_to_run(compose_file_path)
        #
        # print("Running the Jenkins container...")
        # subprocess.run(docker_run_command, check=True)
        # print("Jenkins has been deployed. Access it at http://localhost:8080")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
