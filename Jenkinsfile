pipeline {
  agent any
  stages {
    stage('Checkout Code from GIT') {
      steps {
        git(url: 'https://github.com/rutvik2611/Ninja', branch: 'working')
      }
    }

    stage('Prepare and Run cutcut service') {
      steps {
        script {
          // Navigate to the correct service directory
          dir('src/services/cutcut') {

            // Print all files in the 'cutcut' service directory to verify their presence
            sh 'echo "Verifying presence of necessary files:"'
            sh 'ls -l' // This will list all the files in the current directory

            // Build the Docker image from the Dockerfile in the current directory
            // and tag it as 'cutcut'. It assumes the context is the current directory ('.')
            sh 'echo "Building Docker image..."'
            sh 'sudo docker build -t cutcut .' // You may replace 'cutcut' with any tag you prefer

            // After building, run the created image using a Docker run command.
            // This is a basic example; you may need to adjust it as per your application's requirements.
            sh 'echo "Running Docker image..."'
            sh 'docker run -d --name cutcut_instance -p desired_port:internal_port cutcut' // Replace 'desired_port' and 'internal_port' with your actual ports
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
