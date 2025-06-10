FROM jenkins/jenkins:jdk21

LABEL maintainer="tysonhoang"
LABEL description="Jenkins with JDK 21 and preinstalled plugins for cloud-based CI/CD pipeline solution"

# Skip setup wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Preinstall required plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Copy init script to create admin user
COPY init.groovy.d/ /usr/share/jenkins/ref/init.groovy.d/
