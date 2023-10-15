# Start from the Jenkins LTS image
FROM jenkins/jenkins:lts

# Switch to root user to install additional software
USER root

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
    usermod -aG docker jenkins  # Removed the backslash, as it's the end of the command

# Adjust permissions for Jenkins home
RUN chown -R jenkins:jenkins /var/jenkins_home

# [Optional] If the jenkins user needs passwordless sudo, uncomment the following line
RUN echo "jenkins ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch back to the jenkins user
USER jenkins

