# Project Yuler
An Django web app that remembers online poker data. Uses said data to helper players make better decisions on when to play. 
## Live site
http://e3726eaab85e.ngrok.io/ignition/chart (Main)
http://2955a2050a6d.ngrok.io/ignition/chart (Backup)
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
- Linear Regression: Regressing Number of players at NL25 on number of players at other stakes, time of day, and day of week. 
- CVXPY Regression: Regressing on the same variables, but using convex solvers to include an inequality constraint, which ensures that predictions for 50+ players will be greater than fifty. 
- Tobit Regression: In progress.  
## Naming
A pun that combines the famous Project Euler, and Udny Yule, the Yule in the Yule-Walker equations from time series analysis. 
