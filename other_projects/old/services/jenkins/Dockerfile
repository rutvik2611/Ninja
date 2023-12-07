# Start from the Jenkins LTS image
FROM jenkins/jenkins:lts

# Switch to root user to install additional software
USER root

# Note to users: You need to comment/uncomment the DOCKER_HOST environment variable
# based on your environment. The default is set for Docker on Windows.
# For Linux, you might not need to set this variable, or it could be different.

# ----------------- WINDOWS CONFIGURATION START -----------------
# For Docker Desktop on Windows, uncomment the following line:
ENV DOCKER_HOST=tcp://host.docker.internal:2375
# ----------------- WINDOWS CONFIGURATION END -------------------

# ----------------- LINUX CONFIGURATION START -------------------
# For Docker on Linux, comment out the above line, and if needed, uncomment and set the following line:
# ENV DOCKER_HOST=tcp://<your-linux-docker-host>:2375
# ----------------- LINUX CONFIGURATION END ---------------------

# Install prerequisite software
RUN apt-get update && \
    apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg2 \
      software-properties-common

# Add Docker's official GPG key and repository
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/debian \
    $(lsb_release -cs) \
    stable"

# Install Docker and Docker Compose
RUN apt-get update && \
    apt-get install -y docker-ce-cli && \
    curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose

# Create the 'docker' group and add the 'jenkins' user to it
RUN groupadd docker && \
    usermod -aG docker jenkins

# Adjust permissions for Jenkins home
RUN chown -R jenkins:jenkins /var/jenkins_home

# [Optional] If the jenkins user needs passwordless sudo, uncomment the following line
# This line is optional and should be used with caution, especially in production environments
RUN echo "jenkins ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch back to the jenkins user
USER jenkins
