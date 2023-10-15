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
        sh 'docker --version' // Just to confirm that Docker is available
        sh 'ls -al'
        sh 'find .'

        // Build the Docker image within the Jenkins pipeline and tag it
        def cutcutImage = docker.build('cutcut', '-f Dockerfile .')  // Ensure this command points to your actual Dockerfile location and context

        // Now, run your docker-compose up command. This assumes your docker-compose file is set up correctly.
        // The Jenkins workspace path is prepended to your compose file's services' build context and should be considered in the paths within your compose file.
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
