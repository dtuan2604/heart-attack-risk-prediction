import jenkins.model.*
import org.jenkinsci.plugins.workflow.job.WorkflowJob
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import hudson.plugins.git.*
import hudson.scm.*

def instance = Jenkins.getInstance()

def jobName = System.getenv("JENKIN_JOB_NAME") ?: "my-auto-pipeline"
def repoUrl = System.getenv("REPO_URL") ?: "jenkins"
def credentialsId = "github-token"

if (instance.getItem(jobName) == null) {
    def job = instance.createProject(org.jenkinsci.plugins.workflow.job.WorkflowJob, jobName)

    def scm = new GitSCM(
        GitSCM.createRepoList(repoUrl, credentialsId),
        [new BranchSpec("*/release")],
        false, Collections.<SubmoduleConfig>emptyList(),
        null, null, []
    )

    def definition = new CpsScmFlowDefinition(scm, "Jenkinsfile")
    job.setDefinition(definition)
    job.addTrigger(new com.cloudbees.jenkins.GitHubPushTrigger())
    job.save()
}

println "jenkin_job_name: ${jobName}"
println "repo_url: ${repoUrl}"

instance.save()
