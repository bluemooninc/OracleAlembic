FROM centos:centos6.7

ENV container docker

# Local setup
RUN cp -p /etc/localtime /etc/localtime.org
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN cp -p /etc/sysconfig/clock /etc/sysconfig/clock.org
RUN echo 'ZONE="Asia/Tokyo"' > /etc/sysconfig/clock

# yum
RUN yum -y install yum-plugin-ovl
RUN yum -y update
RUN yum -y reinstall glibc-common
RUN yum -y clean all
RUN yum -y install httpd httpd-devel gcc* make tar bzip2 wget which vim
RUN yum -y install m4 dbus file giflib
RUN yum -y install java-1.7.0-openjdk java-1.7.0-openjdk-devel libaio
RUN yum -y install rsync rsyslog
RUN yum -y install tcp_wrappers tcpdump
RUN yum -y install unzip

# ssh install
RUN yum -y install openssh-server openssh-clients && \
    mkdir  ~/.ssh && \
    touch  ~/.ssh/authorized_keys && \
    chmod 600  ~/.ssh/authorized_keys

# SSHD
RUN sed -ri 's/^UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

###################
# python3.6
###################
RUN yum install -y https://centos6.iuscommunity.org/ius-release.rpm
RUN yum install -y python36*
RUN ln -s /usr/bin/python3.6 /usr/bin/python3
RUN ln -s /usr/bin/pip3.6 /usr/bin/pip3
RUN pip3 install --upgrade pip

###################
# Install cx_Oracle
###################
RUN mkdir -p /tmp
COPY oracle-instantclient18.3-basic-18.3.0.0.0-1.x86_64.rpm /tmp/
COPY oracle-instantclient18.3-sqlplus-18.3.0.0.0-1.x86_64.rpm /tmp/
ENV ORACLE_HOME /usr/lib/oracle/18.3/client64
ENV ORACLE_SID orcl
ENV LD_RUN_PATH $ORACLE_HOME
ENV LD_LIBRARY_PATH $ORACLE_HOME/lib
ENV PATH=$ORACLE_HOME/bin:$PATH
ENV TNS_ADMIN $ORACLE_HOME/network/admin
RUN cd /tmp && \
    rpm -ivh oracle-instantclient18.3-basic-18.3.0.0.0-1.x86_64.rpm && \
    rpm -ivh oracle-instantclient18.3-sqlplus-18.3.0.0.0-1.x86_64.rpm && \
    ln -s $LD_LIBRARY_PATH/libclntsh.so.18.1 $LD_LIBRARY_PATH/libclntsh.so && \
    rm *.rpm

RUN pip3 install cx_Oracle

RUN mkdir $ORACLE_HOME/network/admin -p
RUN echo "orcl=\
          (DESCRIPTION=\
            (ADDRESS=\
              (PROTOCOL=TCP)(HOST=oracle-container)(PORT=1521)\
            )\
            (CONNECT_DATA =\
              (SERVER=DEDICATED)\
              (SID=orcl)\
              (SERVICE_NAME=pdb1)\
            )\
          )" >> /usr/lib/oracle/18.3/client64/network/admin/tnsnames.ora

#####################
# Install SQL Alchemy
#####################
RUN pip3 install sqlalchemy

#################
# Install Alembic
#################
ENV ALEMBIC_VERSION='1.0.0'
RUN pip3 install --no-cache-dir alembic==$ALEMBIC_VERSION

# initializing
RUN chkconfig iptables off
RUN /etc/init.d/iptables stop

EXPOSE 22

CMD ["bash"]
