FROM jenkins/jenkins:jdk17

LABEL maintainer="tysonhoang"
LABEL description="Jenkins with JDK 21 and preinstalled plugins for cloud-based CI/CD pipeline solution"

# Skip setup wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

USER root
RUN curl https://get.docker.com > dockerinstall && \
    chmod 777 dockerinstall && \
    ./dockerinstall && \
    usermod -aG docker jenkins

RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

USER jenkins

# Preinstall required plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Copy init script to create admin user
COPY init.groovy.d/ /usr/share/jenkins/ref/init.groovy.d/
