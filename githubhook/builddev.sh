echo "URL"
echo $1

echo "Branch"
echo $2

rm -rf /build/*
cd /build
git clone $1

cd AtlasFalls
git checkout $2

git pull

# exit 1
cp /AtlasFalls/githubhook/mysql_config.cpp.dev /build/AtlasFalls/AwakeMUD/src/mysql_config.cpp

cd /build/AtlasFalls/AwakeMUD/src
make

rm -rf /AtlasFallsDev/AwakeMUD/bin/awakedev

cp ../bin/awake /AtlasFallsDev/AwakeMUD/bin/awakedev

pkill awakedev
