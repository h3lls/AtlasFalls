#!/bin/sh

/sbin/entrypoint.sh &

# until pids=$(pidof mysqld)
# do   
#     sleep 1
# done
sleep 8
# ps ax
# ls /
# ls /AtlasFalls

# FILE=/usr/lib/libsodium.so.23
# if [ ! -f "$FILE" ]; then
# cd /AtlasFalls/libsodium-1.0.18-RELEASE/
# ./configure
# make && make check
# make install
# ln -s /usr/local/lib/libsodium.so /usr/lib/libsodium.so.23

echo "SQL"
cd /AtlasFalls/AwakeMUD/SQL
/bin/bash ./gensql.sh
cat mysql_config.cpp
cp mysql_config.cpp ../src

cd /AtlasFalls/AwakeMUD/src
make
cd /AtlasFalls/AwakeMUD/
#ps aux
./bin/awake