# Whack

Contains the Python code implementing Flask microframework to build a basic web application that translates images with texts (e.g. restaurant menus, memes, billboard, etc). This web application takes the image URL as input and outputs the text detected from the image and the translation to the desired language.

##### Important
- Must first set up Google Application Credentials and store the json key on user's computer.
- Then set the `os.environ['GOOGLE_APPLICATION_CREDENTIALS']` on `translameme.py` to be the path to that json file.
