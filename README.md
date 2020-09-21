# Project Yuler
An Django web app that remembers online poker data. Uses said data to helper players make better decisions on when to play. 
## Live site
http://54ab765a3bf6.ngrok.io/ignition/
## System Diagram
![alt text](readme_static/project_yuler_system_diagram_v1.PNG)
## How It Works
- Terminal script on Windows captures screenshot of the poker GUI information.
- Image processing to "clean" the screenshot into an image that resembles a spreadsheet.
- PyTesseract OCR to parse the image into integers and floats.
- Django Celery Task that inputs the values into a database at a minute resolution.
- Chart.js to display the most recent 2 hours of data at each stake.
- ngrok forwards my locally running port to the outside world.
## Data Analysis
Finally, after all that hard work building the infrastructure, and perfecting the OCR, here comes the fun part. How do we use the data that we so painstakingly collected and stored to gain some insight, and make some $$$? Before we can solve the question, we first have to ask it. What is it that we are interested in? We can start with a simple observation.
- Observation: It seems that I make more money playing when there are more people online. 
My hand tracking software proves this, and this is probably because the number of people online skyrocket around the evening hours, when people get off their day jobs and want to kick back with a beer, and unwind with some poker.
- The problem: But the issue is, the poker software knows that this is true, and so they purposely obfuscate their data. When the number of people at a particular stake are >50, they just put "50+" instead of the actual number. Using the data we have, how can we best predict the number of people playing at a stake?
- The model: Let's start simple. Linear model. We have 5 different stakes, so we have the variables \[n_1,n_2,n_3,n_4,n_5\]
## Naming
A pun that combines the famous Project Euler, and Udny Yule, the Yule in the Yule-Walker equations from time series analysis. 
