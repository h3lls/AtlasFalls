echo "URL"
echo $1

echo "Branch"
echo $2

rm -rf /build/*
cd /build
git clone $1

git checkout $2

git pull

cp /AtlasFalls/githubhook/mysql_config.cpp.dev /build/AtlasFalls/AwakeMUD/src/mysql_config.cpp

cd /build/AtlasFalls/AwakeMUD/src
make
