from flask import Flask, render_template, flash, request, redirect, url_for
from get_recommendations import *
from posters import *

app = Flask(__name__)
app.secret_key = 'supersecretmre'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recommender', methods=['GET','POST'])
def forminput():
    movies_name = df['names'].head(10).values
    genre_name = df['genre'].head(4).values
    return render_template('form.html', movies_name=movies_name, genre_name=genre_name)


@app.route('/results', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        try:
            name = request.form['name']
            by = request.form['by']
            count = request.form['count']
            print(f'name: {name}, by: {by}, count: {count}')
            count = int(count)
            match by:
                case 'name':
                    movies = get_recommendations(name, count=count)
                case 'word':
                    movies = get_recommendations(name, count=count)
            if movies.empty:
                flash('No movies available', 'danger')
                return redirect(url_for('forminput'))
            
            if 'Movie not found' in movies.values:
                flash('Movie not found', 'danger')
                return redirect(url_for('forminput'))
            else:
                results = [movie_data_from_tmdb(movie) for movie in movies]
                return render_template('results.html', name=name, by=by, count=count, results=results)
        except Exception as e:
            flash('No similar movies found in dataset', 'danger')
            return redirect(url_for('forminput'))
        
    return redirect(url_for('forminput'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)