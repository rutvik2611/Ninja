pipeline {
  agent any

  stages {
    stage('Checkout Code from GIT') {
      steps {
        git(url: 'https://github.com/rutvik2611/Ninja', branch: 'working')
      }
    }

    stage('Validate Environment and Build Docker Image') {
      steps {
        script {
          // Navigate to the directory containing the Dockerfile
          dir('src/services/cutcut') { // Adjust if your path differs
            // Check if the 'docker' command is available
            sh 'docker --version || { echo "Docker is not available, install Docker"; exit 1; }'

            // Check the current user (expected to be 'jenkins' or whichever user has Docker permissions)
            sh 'whoami || { echo "Cannot determine the current user"; exit 1; }'

            // List the contents of the current directory to verify the Dockerfile is present
            sh 'ls -l || { echo "Cannot list the files in the current directory"; exit 1; }'

            // Check if the current user is part of the 'docker' group
            sh 'groups || { echo "Cannot determine the groups the current user belongs to"; exit 1; }'

            // Attempt to build the Docker image
            // 'cutcut' is the tag for your image
            sh 'docker build -t cutcut . || { echo "Docker image build failed"; exit 1; }'
          }
        }
      }
    }

    // Add additional stages as per your process
    // For example, you might have a test stage, deploy stage, etc.
  }

  post {
    always {
      // Actions to perform after the pipeline has finished its execution.
      echo 'Pipeline has finished executing.'
    }
  }
}
