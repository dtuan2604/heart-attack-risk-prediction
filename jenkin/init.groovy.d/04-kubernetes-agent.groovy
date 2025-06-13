import jenkins.model.*
import org.csanchez.jenkins.plugins.kubernetes.*

def serverUrl = System.getenv("K8S_SERVER_URL")
def caCert = System.getenv("K8S_CA_CERT").replace("\\n", "\n")

def nameSpace = System.getenv("K8S_NAMESPACE") ?: "model-serving"
def jenkinsUrl = System.getenv("JENKINS_URL")
def jenkinsTunnel = System.getenv("JENKINS_TUNNEL")


def k8sCloud = new KubernetesCloud("kubernetes")

k8sCloud.setServerUrl(serverUrl)
k8sCloud.setNamespace(nameSpace)
k8sCloud.setServerCertificate(caCert)
k8sCloud.setSkipTlsVerify(false)
k8sCloud.setJenkinsUrl(jenkinsUrl)
k8sCloud.setJenkinsTunnel(jenkinsTunnel)
k8sCloud.setContainerCapStr("10")
k8sCloud.setRetentionTimeout(5)
k8sCloud.setCredentialsId("jenkins-deployer")

Jenkins.instance.clouds.removeAll { it.name == "kubernetes" }
Jenkins.instance.clouds.add(k8sCloud)
Jenkins.instance.save()
