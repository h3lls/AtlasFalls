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

cp /AtlasFalls/githubhook/mysql_config.cpp.dev /build/AtlasFalls/AwakeMUD/src/mysql_config.cpp

cd /build/AtlasFalls/AwakeMUD/src
make

rm -rf /AtlasFallsDev/AwakeMUD/bin/awakedev
rm -rf /AtlasFallsDev/AwakeMUD/lib/
rm -rf /AtlasFallsDev/AwakeMUD/doc/

mkdir -p /AtlasFallsDev/AwakeMUD/bin/ && cp ../bin/awake /AtlasFallsDev/AwakeMUD/bin/awakedev
mkdir -p /AtlasFallsDev/AwakeMUD/lib/ && cp -r ../lib/ /AtlasFallsDev/AwakeMUD/lib/
mkdir -p /AtlasFallsDev/AwakeMUD/doc/ && cp -r ../doc/ /AtlasFallsDev/AwakeMUD/doc/

pkill awakedev
