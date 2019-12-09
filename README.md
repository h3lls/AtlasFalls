# Atlas Falls

# Testing in docker

- Install docker.
- Open a terminal / command window
- Clone this repo to your favorite directory
- (Ensure unix LF style line endings when editing any files in your favorite editor.)
- Run: docker build -t atlasfalls .
- Wait
- Wait even more
- (Windows) Open docker settings and click "Shared Drives" Share the drive that contains your code by ticking the checkbox for that drive.
- To test your code (Example path that you shared from windows is G and should point to your source code): 
	docker run -p 4000:4000 -v G:\Projects\AthensWell:/AtlasFalls -it atlasfalls "/dockerstartmud.sh"
- Connect to your mud on localhost port 4000

# New server install
- Crontab entries:
```
* * * * * pgrep -x awake >/dev/null || cd /AtlasFalls/AwakeMUD && bin/awake 4000 >/dev/null 2>&1 && echo "Starting prod server"
* * * * * pgrep -x awakedev >/dev/null || cd /AtlasFallsDev/AwakeMUD && bin/awakedev 4001 >/dev/null 2>&1 && echo "Starting dev server"
* * * * * ps -ef | grep bot.py | grep -v grep >/dev/null || cd /AtlasFalls/discordbot && python3 bot.py
* * * * * ps -ef | grep hook.py | grep -v grep >/dev/null || cd /AtlasFalls/githubhook && python3 hook.py
```

*THIS DOES NOT PERSIST THE DATABASE.*
