pipeline {
  agent any
  stages {
    stage('Checkout Code from GIT') {
      steps {
        git(url: 'https://github.com/rutvik2611/Ninja', branch: 'working')
      }
    }

    // Removed 'Setup Python Environment' and 'Execute Python Script' stages as per your request.

    stage('Build and Run cutcut service') {
      steps {
        script {
          // Change the directory to the location of the Dockerfile for the cutcut service.
          dir('services/cutcut') {
            // Build the Docker image, tagging it as 'cutcut'.
            // 'docker.build' is provided by the Docker Pipeline plugin.
            def cutcutImage = docker.build('cutcut')

            // Run the cutcut service. This will use the 'docker-compose' command,
            // assuming your docker-compose file is set up to run the service with the newly built image.
            // The 'sh' step is used to execute the shell command.
            sh 'docker-compose -f cutcut-docker-compose.yml up -d'
          }
        }
      }
    }

    // Additional stages can be added here.

  }
  post {
    always {
      // Actions to perform after the pipeline has finished.
      echo 'Pipeline has finished executing.'
    }
  }
}
