FROM centos:7

RUN yum update -y && yum install -y epel-release openssh-clients git docker
RUN yum install -y python-pip python3
