from flask import Flask, render_template, session, g, redirect, request,\
    url_for
from flask_bootstrap import Bootstrap #changed the module's name
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import Required, Length
# for detect text
import os
from google.cloud import vision
from google.protobuf import json_format


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class ImageToText():

    @staticmethod
    def detect_text_uri(uri):
        """Detects text in the file located in Google Cloud Storage or on the Web.
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"D:\Wellesley College\Fall'19\WHACK\\key\whack-a6d2eb6d8294.json"
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.text_detection(image=image) # outputs json
        # print(response)
        texts = response.text_annotations
        # print(texts)
        result = texts[0].description
        # print('Texts:')
        # print(result)
        return result
    
    @staticmethod
    def translateText(text, target):
        # Imports the Google Cloud client library
        from google.cloud import translate_v2 as translate
        import os

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"D:\Wellesley College\Fall'19\WHACK\\key\whack-a6d2eb6d8294.json"

        # Instantiates a client
        translate_client = translate.Client()

        # The text to translate
        text = text
        # The target language
        target = target

        # Translates some text into Russian
        translation = translate_client.translate(
            text,
            target_language=target)
        result = translation['translatedText']
        # print(u'Text: {}'.format(text))
        # print(u'Translation: {}'.format(translation['translatedText']))
        return result

class ImageAndLangForm(Form):
    path = StringField('Enter the URL to image',
        validators=[Required(), Length(1,1000)])
    lang = StringField('Enter target language',
        validators=[Required(), Length(1,2)])
    submit = SubmitField('Submit')
    @staticmethod
    def getPath(form):
        return form.path
    @staticmethod
    def getLang(form):  
        return form.lang

@app.route('/')
def index():
    return(render_template('mainPage.html'))

@app.route('/submitImagePath', methods= ['GET','POST'])
def submitImagePath():
    translation = None
    text = None
    form = ImageAndLangForm()
    if form.validate_on_submit():
        imgPath = str(form.path.data)
        targetLang = str(form.lang.data)
        text = ImageToText.detect_text_uri(imgPath)
        translation = ImageToText.translateText(text,targetLang)
    return(render_template('submitPath.html', form=form, text=text, translation=translation))

    
if __name__ == '__main__':
    app.run(debug=True)
    