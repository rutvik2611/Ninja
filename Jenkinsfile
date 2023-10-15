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
      dir('services/cutcut') {
        // Check if Docker is available
        sh 'docker --version' // This line is for debugging. If this command fails, then Docker is not installed on this agent.

        // If the above command succeeds but the next steps fail, it is likely an issue with the Docker Pipeline plugin.
        def cutcutImage = docker.build('cutcut')

        // After building, you can run your image. Adjust the docker run command according to your setup.
        // This is a basic example, and you may need additional parameters based on your docker-compose file.
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
