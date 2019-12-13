FROM centos:7

RUN yum update -y && yum install -y epel-release openssh-clients git docker
RUN yum install -y python-pip
RUN pip install ansible==2.9.2
