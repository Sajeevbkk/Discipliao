from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from db import db
from datetime import datetime

add_bp = Blueprint('add', __name__, url_prefix='/add')

@add_bp.route('/')
@login_required
def index():
    return render_template('add_index.html')

@add_bp.route('/subject', methods=['GET', 'POST'])
@login_required
def add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        try:
            priority = int(request.form.get('priority'))
            if not (1 <= priority <= 10):
                raise ValueError
        except ValueError:
            flash('Priority must be an integer between 1 and 10.', 'danger')
            return redirect(url_for('add.add_subject'))

        db.add_subject(name, priority)
        flash('Subject added successfully!', 'success')
        return redirect(url_for('add.index'))
    return render_template('add_subject.html')

@add_bp.route('/chapter', methods=['GET', 'POST'])
@login_required
def add_chapter():
    subjects = db.get_subjects()
    if request.method == 'POST':
        name = request.form.get('name')
        subject_id = request.form.get('subject_id')

        if not subject_id:
            flash('You must select a subject.', 'danger')
            return redirect(url_for('add.add_chapter'))

        db.add_chapter(name, subject_id)
        flash('Chapter added successfully!', 'success')
        return redirect(url_for('add.index'))
    return render_template('add_chapter.html', subjects=subjects)

@add_bp.route('/topic', methods=['GET', 'POST'])
@login_required
def add_topic():
    subjects = db.get_subjects()

    subject_id = request.args.get('subject_id') or request.form.get('subject_id')
    chapters = []
    if subject_id:
        chapters = db.get_chapters(subject_id)

    if request.method == 'POST' and request.form.get('action') == 'add':
        name = request.form.get('name')
        chapter_id = request.form.get('chapter_id')
        currently_studying = True if request.form.get('currently_studying') == 'on' else False
        completed = True if request.form.get('completed') == 'on' else False
        try:
            priority = int(request.form.get('priority'))
            if not (1 <= priority <= 10):
                raise ValueError
        except ValueError:
            flash('Priority must be an integer between 1 and 10.', 'danger')
            return redirect(url_for('add.add_topic', subject_id=subject_id))

        if not chapter_id:
            flash('You must select a chapter.', 'danger')
            return redirect(url_for('add.add_topic', subject_id=subject_id))

        db.add_topic(name, chapter_id, currently_studying, completed, priority)
        flash('Topic added successfully!', 'success')
        return redirect(url_for('add.add_topic', subject_id=subject_id, chapter_id=chapter_id))

    chapter_id = request.args.get('chapter_id') or request.form.get('chapter_id')
    return render_template('add_topic.html', subjects=subjects, chapters=chapters, selected_subject_id=subject_id, selected_chapter_id=chapter_id)

@add_bp.route('/day', methods=['GET', 'POST'])
@login_required
def add_day():
    if request.method == 'POST':
        name = request.form.get('name')
        db.add_day(name)
        flash('Day added successfully!', 'success')
        return redirect(url_for('add.index'))
    return render_template('add_day.html')

@add_bp.route('/time', methods=['GET', 'POST'])
@login_required
def add_time():
    days = db.get_days()
    if request.method == 'POST':
        day_id = request.form.get('day_id')
        from_time = request.form.get('from_time')

        if not day_id:
            flash('You must select a day.', 'danger')
            return redirect(url_for('add.add_time'))

        try:
            from_time_obj = datetime.strptime(from_time, "%I:%M%p")
        except ValueError:
            try:
                # Fallback to standard time input type format "HH:MM"
                from_time_obj = datetime.strptime(from_time, "%H:%M")
            except ValueError:
                flash('Invalid time format.', 'danger')
                return redirect(url_for('add.add_time'))

        db.add_time(from_time_obj.hour, from_time_obj.minute, day_id)
        flash('Time added successfully!', 'success')
        return redirect(url_for('add.index'))
    return render_template('add_time.html', days=days)
