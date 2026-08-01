from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from db import db

edit_bp = Blueprint('edit', __name__, url_prefix='/edit')

@edit_bp.route('/')
@login_required
def index():
    subjects = db.get_subjects()
    days = db.get_days()
    return render_template('edit_index.html', subjects=subjects, days=days)

@edit_bp.route('/subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    subject = db.get_subject(subject_id)
    if not subject:
        flash('Subject not found.', 'danger')
        return redirect(url_for('edit.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        try:
            priority = int(request.form.get('priority'))
            if not (1 <= priority <= 10):
                raise ValueError
        except ValueError:
            flash('Priority must be an integer between 1 and 10.', 'danger')
            return redirect(url_for('edit.edit_subject', subject_id=subject_id))

        db.edit_subject(subject_id, name, priority)
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('edit.index'))
    return render_template('edit_subject.html', subject=subject)

@edit_bp.route('/chapter/<int:chapter_id>', methods=['GET', 'POST'])
@login_required
def edit_chapter(chapter_id):
    chapter = db.get_chapter(chapter_id)
    if not chapter:
        flash('Chapter not found.', 'danger')
        return redirect(url_for('edit.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        db.edit_chapter(chapter_id, name)
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('edit.index'))
    return render_template('edit_chapter.html', chapter=chapter)

@edit_bp.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
@login_required
def edit_topic(topic_id):
    topic = db.get_topic(topic_id)
    if not topic:
        flash('Topic not found.', 'danger')
        return redirect(url_for('edit.index'))

    subjects = db.get_subjects()
    chapter = db.get_chapter(topic[2]) # topic[2] is chapter_id
    subject_id = chapter[2] if chapter else request.form.get('subject_id')
    chapters = []

    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        if request.form.get('action') == 'update_subject':
            chapters = db.get_chapters(subject_id) if subject_id else []
        elif request.form.get('action') == 'update_topic':
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
                return redirect(url_for('edit.edit_topic', topic_id=topic_id))

            if not chapter_id:
                flash('You must select a chapter.', 'danger')
                return redirect(url_for('edit.edit_topic', topic_id=topic_id))

            db.edit_topic(topic_id, name, chapter_id, currently_studying, completed, priority)
            flash('Topic updated successfully!', 'success')
            return redirect(url_for('edit.index'))
    else:
        if subject_id:
            chapters = db.get_chapters(subject_id)

    return render_template('edit_topic.html', topic=topic, subjects=subjects, chapters=chapters, selected_subject_id=subject_id)

@edit_bp.route('/day/<int:day_id>', methods=['GET', 'POST'])
@login_required
def edit_day(day_id):
    day = db.get_day(day_id)
    if not day:
        flash('Day not found.', 'danger')
        return redirect(url_for('edit.index'))

    if request.method == 'POST':
        name = request.form.get('name')
        db.edit_day(day_id, name)
        flash('Day updated successfully!', 'success')
        return redirect(url_for('edit.index'))
    return render_template('edit_day.html', day=day)

@edit_bp.route('/time/<int:time_id>', methods=['GET', 'POST'])
@login_required
def edit_time(time_id):
    time = db.get_time(time_id)
    if not time:
        flash('Time not found.', 'danger')
        return redirect(url_for('edit.index'))

    if request.method == 'POST':
        from_time = request.form.get('from_time')
        try:
            from_time_obj = datetime.strptime(from_time, "%I:%M%p")
        except ValueError:
            try:
                from_time_obj = datetime.strptime(from_time, "%H:%M")
            except ValueError:
                flash('Invalid time format.', 'danger')
                return redirect(url_for('edit.edit_time', time_id=time_id))

        db.edit_time(time_id, from_time_obj.hour, from_time_obj.minute)
        flash('Time updated successfully!', 'success')
        return redirect(url_for('edit.index'))

    from datetime import datetime as dt, time as t
    time_str = dt.combine(dt.today(), t(time[1], time[2])).strftime("%H:%M")
    return render_template('edit_time.html', time=time, time_str=time_str)

@edit_bp.route('/subject/<int:subject_id>/chapters')
@login_required
def list_chapters(subject_id):
    chapters = db.get_chapters(subject_id)
    subject = db.get_subject(subject_id)
    return render_template('edit_list_chapters.html', chapters=chapters, subject=subject)

@edit_bp.route('/chapter/<int:chapter_id>/topics')
@login_required
def list_topics(chapter_id):
    topics = db.get_topics(chapter_id)
    chapter = db.get_chapter(chapter_id)
    return render_template('edit_list_topics.html', topics=topics, chapter=chapter)

@edit_bp.route('/day/<int:day_id>/times')
@login_required
def list_times(day_id):
    times = db.get_times(day_id)
    day = db.get_day(day_id)

    formatted_times = []
    from datetime import datetime as dt, time as t
    for time_rec in times:
        t_str = dt.combine(dt.today(), t(time_rec[1], time_rec[2])).strftime("%I:%M%p")
        formatted_times.append((time_rec[0], t_str))

    return render_template('edit_list_times.html', times=formatted_times, day=day)
