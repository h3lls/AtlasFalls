# Atlas Falls

# Testing in docker

- Install docker
- Open a terminal / command window
- Clone this repo to your favorite directory
- (Ensure unix LF style line endings when editing any files in your favorite editor.)
- Run: docker build -t atlasfalls .
- Wait...
- Wait even more
- (Windows) Open docker settings and click "Shared Drives" Share the drive that contains your code by ticking the checkbox for that drive.
- To test your code (Example path that you shared from windows is G and should point to your source code): 
	docker run -p 4000:4000 -v G:\Projects\AthensWell:/AtlasFalls -it atlasfalls "/dockerstartmud.sh"
- Connect to your mud on localhost port 4000


*THIS DOES NOT PERSIST THE DATABASE.*
