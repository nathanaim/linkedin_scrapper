## Introduction

This repository aims at automating the scrapping of Linkedin profiles. It is set up on Firefox but can be adapted to any other browser easily. <br/>
Currently the scrapper gets the name, title, experiences and educations of the profile which is given, but you could scrap virtually anything on the profile using the same logic which is displayed here. <br/>

## Set up

You can use this repository with your own Linkedin profile but I strongly advise against it as Linkedin could take your profile down. <br/>

Instead I highly recommend you create a Linkedin profile dedicated to the scrapping of other profiles. <br/>

### Creating a Linkedin profile

For Linkedin not to strike down your profile you need to make it look as real as possible. <br/>
You will definitely need a mail (some sites allow you to create a mail address in minutes).
You should then pimp your profile as much as possible : add a picture (from a non existent person, similarly this can easily be found online), add education, add experiences (freelancing is convenient as you would not need to claim you've worked for a real company), connect with people at random... <br/>

It appears such profiles are less likely to be taken down by Linkedin, hence the advice. <br/>

### Associate this Linkedin profile to a Firefox profile

The Firefox documentation tells you how to manage different Firefox profiles. Log in on Linkedin on a specific Firefox profile with the Linkedin profile you created earlier. <br/>
You will then need to locate it on your computer (this is something like 'C:\Users\username\AppData\Roaming\Mozilla\Firefox\Profiles\profilename') and put the path in the config.yml file.

### Scrap profiles

In the right environment (see requirements.txt), you can use the script this way : <br/>
```python lk_scrapper.py linkedinprofileurl``` <br/>

A Profile instance is then created, containing the name, title, experiences and educations of the profile which was given. <br/>
Currently the script only prints to the terminal what it scrapped, but obviously you could do much more interesting things with it, such as sending it to your favorite CRM, or creating automated summary for every candidate for which you have the Linkedin URL.