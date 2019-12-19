#!groovy

node {
    try {
        def registry = "dl2.homeawaycorp.com"
        def org = "analyticsengineering"
        def repo = "ae-audatar"
        def app = "${org}/${repo}"
        def branch = env.BRANCH_NAME

        def repo_flask = "ae-audatar-flask"
        def repo_node = "ae-audatar-node"
        def repo_celery = "ae-audatar-celery"
        def app_flask = "${org}/${repo_flask}"
        def app_node = "${org}/${repo_node}"
        def app_celery = "${org}/${repo_celery}"

        def slackChannel = "#audatar"

        stage("Checkout") {
            checkoutProject()
        }

        stage("Build Docker Image") {
            sh "./docker-build.sh"
        }

        stage("Update Version") {
            sh "./update-version.sh ${branch}-${getCommitHash()}"
        }

        stage("Create Docker Tags") {
            sh "docker tag ${registry}/${app_flask} ${registry}/${app_flask}:${branch}-${getCommitHash()}"
            sh "docker tag ${registry}/${app_node} ${registry}/${app_node}:${branch}-${getCommitHash()}"
            sh "docker tag ${registry}/${app_celery} ${registry}/${app_celery}:${branch}-${getCommitHash()}"
        }

        stage("Publish Docker Image to Docker-Local") {
            publishDockerImage(imageName: app_flask, tags: ["latest","${branch}-${getCommitHash()}"])
            publishDockerImage(imageName: app_node, tags: ["latest","${branch}-${getCommitHash()}"])
            publishDockerImage(imageName: app_celery, tags: ["latest","${branch}-${getCommitHash()}"])
        }

        stage("Publish Docker Image to Docker-Releases") {
            if (branch == "release") {
                cdDockerPromote(githubOwner: org, githubRepo: repo, dockerImageVersion: "${app_flask}:${branch}-${getCommitHash()}")
                cdDockerPromote(githubOwner: org, githubRepo: repo, dockerImageVersion: "${app_node}:${branch}-${getCommitHash()}")
                cdDockerPromote(githubOwner: org, githubRepo: repo, dockerImageVersion: "${app_celery}:${branch}-${getCommitHash()}")
            }
        }

        stage("Notify Slack") {
            notifySlack (
                title: "${env.JOB_NAME} ${env.BUILD_NUMBER} successfully deployed to MoT",
                message: "${env.BUILD_URL}",
                channel: slackChannel,
                color: "good")
        }
    } catch (err) {
        mail body: "${env.BUILD_URL}",
            from: 'audatar-jenkins-alerts',
            subject: "${env.JOB_NAME} ${env.BUILD_NUMBER} Failed",
            to: 'analyticsengineeringoperations@groups.homeawaycorp.com'

        notifySlack(
            title: "${env.JOB_NAME} ${env.BUILD_NUMBER} Failed",
            message: "${env.BUILD_URL}",
            channel: "#audatar",
            color: "danger")

        throw err
    }
}
