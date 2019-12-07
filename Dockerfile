FROM ubuntu:16.04

RUN apt-get update

# Install dev environment to compile
RUN apt-get install -y automake make gcc g++ clang libtool autoconf zlib1g-dev libcurl4-openssl-dev libmysqlclient-dev

RUN mkdir /var/run/mysqld/
RUN mkdir /var/lib/mysql/
RUN chmod -R 777 /var/run/mysqld/
RUN chmod -R 777 /var/lib/mysql/

ENV MYSQL_USER=mysql \
    MYSQL_DATA_DIR=/var/lib/mysql \
    MYSQL_RUN_DIR=/run/mysqld \
    MYSQL_LOG_DIR=/var/log/mysql
# Install MySQL.
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server=${MYSQL_VERSION}* \
 && rm -rf ${MYSQL_DATA_DIR} \
 && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /sbin/entrypoint.sh

RUN chmod 755 /sbin/entrypoint.sh

# Define mountable directories.
VOLUME ["/etc/mysql", "/var/lib/mysql"]

ADD ./libsodium-1.0.18-RELEASE/ /AtlasFalls/libsodium-1.0.18-RELEASE/

RUN cd /AtlasFalls/libsodium-1.0.18-RELEASE/ && \
	./configure && \
	make && make check && \
	make install && \
	ln -s /usr/local/lib/libsodium.so /usr/lib/libsodium.so.23


# Define working directory.
WORKDIR /data

ADD dockerstartmud.sh /

RUN chmod +x /dockerstartmud.sh

EXPOSE 3306/TCP
EXPOSE 4000

# Build with: docker build -t atlasfalls . 
# Start with: docker run -p 4000:4000 -v G:\Projects\AthensWell:/AtlasFalls -it atlasfalls "/dockerstartmud.sh"
# Connect to: localhost:4000