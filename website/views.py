from flask import Blueprint, render_template, request, flash, redirect, url_for
import json
from .models import Director
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if(request.form.get('info_name') and request.form.get('info_directorID')):
            director_id = request.form.get('info_directorID')
            name = request.form.get('info_name')
            id = name[name.index('-')+1:]
            name = name[0:name.index('-')]

            entry = Director.query.filter_by(director_id=director_id).first()
            if entry:
                if len(entry.ret_value) == 0:
                    flash('NO SIMILAR DIRECTORS FOUND!', category='error')
                else:
                    entry.count += 1
                    db.session.commit()
                    flash(f"Similar directors have been found {entry.count} times for {name}!", category='success')
                    return render_template('home.html', recs=json.loads(entry.ret_value))
            else:
                movies = (request.form.get(f"info_movies{id}")).split(',')
                from .directorFinder import similarDirectors
                recs = similarDirectors(movies, name)
                new_entry = Director(director_id=director_id, director_name=name, 
                                    ret_value='' if not recs else json.dumps(recs), count=1)
                db.session.add(new_entry)
                db.session.commit()
                if not recs:
                    flash('NO SIMILAR DIRECTORS FOUND!', category='error')
                else:
                    flash(f"This is the first time {name} has been searched for!", category='success')
                    return render_template('home.html', recs=recs)
        else:
            director_name = request.form.get('director_name')
            if len(director_name) < 2:
                flash('Director\'s name must be greater than 1 character.', category='error')
            else:
                from .directorFinder import getDirector
                data = getDirector(director_name)
                if len(data) == 0:
                    flash('DIRECTOR COULDN\'T BE FOUND!', category='error')
                else:
                    return render_template('home.html', data=data)
    
    return render_template('home.html')