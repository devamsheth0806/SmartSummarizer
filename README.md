# Smart Summarizer
This is a Python-based application summarizing content through user-provided queries by applying natural language processing techniques. It is developed under guidance of mentors from Hewlett Packard Enterprise.
This application is containerized with Docker to improve scalability, deployment, and availability.



### Instructions for working with application in Windows 10
Setup for running docker application in Windows 10:

Pre-requisite:
Turn on windows feature for Hyper-V and Windows subsystem for linux

1) Download docker for windows from this link - https://hub.docker.com/editions/community/docker-ce-desktop-windows/

2) Download VcXsrv Windows X server from this link - https://sourceforge.net/projects/vcxsrv/

3) Install the above softwares

4) Following steps are required everytime when the host system is booted:
	a. Launch Xlaunch
	b. Select Multiple Windows option and select next (keep display number as -1)
	c. Select Start no client option and click next
	d. Check all the checkboxes and select next
	e. Save configuration file any where in %userprofile%
	f. Click finish

5) Set 'DISPLAY' variable:
	a. open command prompt and enter ipconfig
	b. copy the IP address of IPv4
	c. open powershell and set 'DISPLAY' variable using the following command:
		set-variable -name DISPLAY -value <IP address>:0.0
	d. Don't close that powershell

6) In that same powershell, enter the following command to run the docker image:
	docker run -v <Path to a folder in your system containing input files>:/usr/src/app/inputFiles -ti -e DISPLAY=$DISPLAY iamrj846/smart2.0:latest

### Instructions for working with application in Linux
To run the application as a docker container in linux system, follow these steps. All the steps are mandatory. 
1) Run the following command on your system.
	xauth list

2) Make sure that the output is of the form 
	username/unix:0 MIT-MAGIC-COOKIE-1 8fe8efc75454dbf178bbe00442689406

3) Copy the above output in a separate file

4) Run the following command.
	sudo docker run -v <Path to a folder in your system containing input files>:/usr/src/app/inputFiles -ti --net=host -e DISPLAY -v /tmp/.X11-unix iamrj846/smart2.0:latest bash

Example path of the folder is: /home/username/Desktop/inputFiles

5) Inside the bash, run the following commands
	a) xauth add <the output pasted in a separate file in step 2>
	b) Verify that the host system is connected to the remote system using this command: xauth list
6) Run the file GUI_1.6.py using the following command.
	a) python3 GUI_1.6.py

NOTE:
If an error such as {_tkinter.TclError: couldn't connect to display ":1"} persists, replace :0 with :1 in the token in step 2.

Instructions for getting access tokens for extracting data from various social media platforms such as Twitter and Facebook:
	
 For Twitter:
		Twitter API uses OAuth, which is an open authorization protocol to authenticate requests. 
		You will need to create and configure your authentication credentials to access Twitter API.
  
  Step 0: Open a Twitter account. If you already have a Twitter account, skip this step.
  
  Step 1: Apply for a developer account  
    - Go to their developer site and go to apply for access and select “Apply for a developer account”. You will be prompted to log in to your Twitter account.  
		- You will then be navigated to a page asking for the usage of the Twitter APIs and data.  
		- Select your choice path and fill the details in the next page and fill in some personal details. When you get to intended use, there are a couple of fields with minimum character limit.  
		- Once you’ve gone through those steps and accept developer agreement, you now have a developer account.	
  
  Step 2: Create an Application  
				- You might have to wait a minute for your developer account to be approved — but once it is, you can start creating your application.  
				- Go to your profile tab and select Apps.  
				  Create an app and fill in the details.  
  
  Step 3: Get your authentication details  
				- Go to your apps page where you will see the app you created. Click on details.  
				- Once you’re there, click on keys and tokens to get the relevant keys. You will need to generate your access token and access token secret. You also have the capability to regenerate the key.  
      `Note: You will need the Consumer key (API key), Consumer Secret (API secret key), Access Token and Access token secret for extracting twitter tweets.`
	
 For Facebook:  
   Step 1: Go to link developers.facebook.com, create an account there.  
   
   Step 2: Go to link developers.facebook.com/tools/explorer.  
   
   Step 3: Go to “My apps” drop down in the top right corner and select “add a new app”. Choose a display name and a category and then “Create App ID”.  
   
   Step 4: Again get back to the same link developers.facebook.com/tools/explorer. You will see “Graph API Explorer” and below “Facebook App” will be there in the right. From “Facebook App” drop down, select your app.  
   
   Step 5: Then, select “User or Page”. From this drop down, select “Get User Access Token”. Select permissions from the menu that appears and then select “Generate Access Token.”  
   
   Step 6: Go to link developers.facebook.com/tools/accesstoken. Select “Debug” corresponding to “User Token”. Go to “Extend Token Access”. This will ensure that your token does not expire every two hours. You will need the Access Token for extracting Facebook posts.
