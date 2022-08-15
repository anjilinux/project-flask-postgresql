from flask import Flask, render_template, request

from wtforms import StringField, SelectField, TextAreaField, validators, Form


import json
from libs.sql_connection import *


class SearchInputs(Form):
    dropdown = SelectField('Searching Criteria', choices = [('Singer', 'singer'),
                                                            ('Song', 'song'),
                                                            ('Lyrics', 'lyrics')],
                                                            validators=[validators.DataRequired()])
    keyword = StringField("Keyword", validators=[validators.DataRequired()])


app = Flask(__name__)
 
 
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods = ['POST', 'GET'])
def search():
    form = SearchInputs(request.form)
    
    if request.method == 'POST' and form.validate():
        dropdown = form.dropdown.data
        keyword = form.keyword.data

        print(dropdown, keyword)

        QUERY = f"SELECT * FROM songtable WHERE LOWER({dropdown}) LIKE '%{keyword}%' LIMIT 20"

        try: 
            df = read_songtable(QUERY)
            df.reset_index(inplace=True)
            return render_template('search.html', form = form, dataframe = json.loads(df.to_json(orient = 'records')))

        except:
            print('there is a problem.')
    return render_template('search.html', form = form)

 

@app.route('/lyrics/<string:id>')
def lyrics(id):
    print(id)

    df = read_songtable(f"SELECT * FROM SONGTABLE WHERE song_id = {id}")
    df['lyrics'] = df['lyrics'].apply(lambda x: x.replace('\n', '<br>'))

    return render_template('lyrics.html', singer = df['singer'][0], song = df['song'][0], album = df['album'][0], lyrics = df['lyrics'][0])


@app.route('/latest')
def latest():
    df = read_songtable('SELECT * FROM SONGTABLE ORDER BY SONG_ID DESC LIMIT 15')
    df.reset_index(inplace = True)

    return render_template('latest.html', dataframe = json.loads(df.to_json(orient = 'records')))

class Songs(Form):
    singer = StringField('Name of the Singer: ', validators=[validators.Length(min=3, max=50), validators.DataRequired()])
    song = StringField('Name of the Song: ', validators=[validators.Length(min=3, max=50), validators.DataRequired()])
    album = StringField('Name of the Album: ', validators=[validators.Length(min=3, max=50), validators.DataRequired()])
    lyrics = TextAreaField('Lyrics of the Song: ', validators=[validators.Length(min=10), validators.DataRequired()])

@app.route('/addnew', methods= ['POST', 'GET'])
def addnew():
    form = Songs(request.form)

    if request.method == 'POST' and form.validate():
        singer = form.singer.data
        song = form.song.data
        album = form.album.data
        lyrics = form.lyrics.data

        print(singer, song, album, lyrics)

        try:
            insert_songtable((singer, song, album, lyrics))

            df = read_songtable(f'SELECT * FROM SONGTABLE ORDER BY SONG_ID DESC LIMIT 20')
            df.reset_index(inplace=True)
            return render_template('latest.html', dataframe = json.loads(df.to_json(orient = 'records')))
        except:
            print('there is a problem')

    return render_template('addnew.html', form = form)


if __name__ == '__main__':
    app.run(port=5000, debug=True)