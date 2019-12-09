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
rm -rf /AtlasFallsDev/AwakeMUD/lib/
rm -rf /AtlasFallsDev/AwakeMUD/doc/

cp ../bin/awake /AtlasFallsDev/AwakeMUD/bin/awakedev
cp -r ../lib/ /AtlasFallsDev/AwakeMUD/lib/
cp -r ../doc/ /AtlasFallsDev/AwakeMUD/doc/

pkill awakedev
