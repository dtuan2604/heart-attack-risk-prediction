import jenkins.model.*
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.impl.*
import com.cloudbees.plugins.credentials.domains.*
import hudson.util.Secret
import org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl

def store = Jenkins.instance.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()

// === GitHub Token Credential ===
def githubToken = System.getenv("GITHUB_TOKEN")
def githubUser = System.getenv("GITHUB_USER") ?: "jenkin"
if (githubToken) {
    def githubCreds = new UsernamePasswordCredentialsImpl(
        CredentialsScope.GLOBAL,
        "github-token",
        "GitHub Personal Access Token",
        githubUser,
        githubToken
    )
    store.addCredentials(Domain.global(), githubCreds)
    println "✔ Added GitHub credentials"
} else {
    println "⚠ GITHUB_TOKEN not provided"
}

// === Docker Hub Credential ===
def dockerUser = System.getenv("DOCKERHUB_USER")
def dockerPass = System.getenv("DOCKERHUB_TOKEN")
if (dockerUser && dockerPass) {
    def dockerCreds = new UsernamePasswordCredentialsImpl(
        CredentialsScope.GLOBAL,
        "dockerhub-creds",            // ID used in your Jenkinsfile
        "Docker Hub Account",
        dockerUser,
        dockerPass
    )
    store.addCredentials(Domain.global(), dockerCreds)
    println "✔ Added Docker Hub credentials"
} else {
    println "⚠ DOCKERHUB_USER or DOCKERHUB_TOKEN not provided"
}

def k8s_token = System.getenv("K8S_TOKEN")

if (k8s_token) {
    def k8sCreds = new StringCredentialsImpl(
        CredentialsScope.GLOBAL,
        "jenkins-deployer",
        "Kubernetes Service Account Token",
        Secret.fromString(k8s_token)
    )
    store.addCredentials(Domain.global(), k8sCreds)
    println "✔ Added Kubernetes token credentials"
} else {
    println "⚠ K8S_TOKEN not provided"
}
