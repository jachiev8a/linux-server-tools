pipeline {
    agent {
        label 'DOCKER'
    }
    
    environment {
        DOCKER_COMPOSE_EXIT_CODE =      0
        EMAIL_DEFAULT =                 "javier.ochoa@osram-continental.com"
    }

    options{timestamps()}

    stages {
        stage('Bootstrap') {
            steps {
                script{
                    currentBuild.displayName = "#${BUILD_NUMBER} - OS-Monitor app"
                    currentBuild.description = "${GIT_BRANCH}<br>${GIT_COMMIT}"
                }
            }
        }
        stage('Deploy App (docker-compose)') {
            steps {
                script {
                    if (DOCKER_COMPOSE_EXIT_CODE == 0) {
                        echo(" > Executing Docker-Compose Up...")
                        sh("./docker-start-app.sh")
                    }
                    else {
                        error("docker-compose is not installed!")
                    }
                }
            }
        }
    } // stages
    
    post {
        failure {
            emailext(
                mimeType: 'text/html',
                subject: "Jenkins Build (No. ${env.BUILD_NUMBER}): - '${env.JOB_NAME}'",
                to: '${EMAIL_DEFAULT}',
                body: """
                <h1>Jenkins: ${env.JOB_NAME} - FAILURE</h1>
                <table style="background-color:#ff5959; border: 3px solid black; border-radius:6px; padding: 10px; padding-right: 80px; padding-left: 80px;">
                    <tr>
                        <th><h2>${currentBuild.result}</h2></th>
                    </tr>
                </table>
                <p>
                    <h2>Jenkins Details</h2>
                    <ul>
                        <li><b>Job Name:</b> ${env.JOB_NAME}</li>
                        <li><b>Job Number:</b> ${env.BUILD_NUMBER}</li>
                    </ul>
                </p>
                <p>Check console output at: <b><a href="${BUILD_URL}/console">${JOB_NAME}/${BUILD_NUMBER}/console</a></b></p>
                <hr>
                <p>Console Log: <b><a href="${BUILD_URL}/consoleText">${JOB_NAME}/${BUILD_NUMBER}/consoleText</a></b></p>
                """
            )

        } // failure
    } // post
} // pipeline
