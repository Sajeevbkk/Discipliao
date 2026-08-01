from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from db import db

delete_bp = Blueprint('delete', __name__, url_prefix='/delete')

@delete_bp.route('/')
@login_required
def index():
    subjects = db.get_subjects()
    days = db.get_days()
    return render_template('delete_index.html', subjects=subjects, days=days)

@delete_bp.route('/subject/<int:subject_id>', methods=['POST'])
@login_required
def delete_subject(subject_id):
    db.delete_subject(subject_id)
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('delete.index'))

@delete_bp.route('/chapter/<int:chapter_id>', methods=['POST'])
@login_required
def delete_chapter(chapter_id):
    chapter = db.get_chapter(chapter_id)
    subject_id = chapter[2] if chapter else None
    db.delete_chapter(chapter_id)
    flash('Chapter deleted successfully!', 'success')
    if subject_id:
        return redirect(url_for('delete.list_chapters', subject_id=subject_id))
    return redirect(url_for('delete.index'))

@delete_bp.route('/topic/<int:topic_id>', methods=['POST'])
@login_required
def delete_topic(topic_id):
    topic = db.get_topic(topic_id)
    chapter_id = topic[2] if topic else None
    db.delete_topic(topic_id)
    flash('Topic deleted successfully!', 'success')
    if chapter_id:
        return redirect(url_for('delete.list_topics', chapter_id=chapter_id))
    return redirect(url_for('delete.index'))

@delete_bp.route('/day/<int:day_id>', methods=['POST'])
@login_required
def delete_day(day_id):
    db.delete_day(day_id)
    flash('Day deleted successfully!', 'success')
    return redirect(url_for('delete.index'))

@delete_bp.route('/time/<int:time_id>', methods=['POST'])
@login_required
def delete_time(time_id):
    time = db.get_time(time_id)
    day_id = time[3] if time else None
    db.delete_time(time_id)
    flash('Time deleted successfully!', 'success')
    if day_id:
        return redirect(url_for('delete.list_times', day_id=day_id))
    return redirect(url_for('delete.index'))

@delete_bp.route('/subject/<int:subject_id>/chapters')
@login_required
def list_chapters(subject_id):
    chapters = db.get_chapters(subject_id)
    subject = db.get_subject(subject_id)
    return render_template('delete_list_chapters.html', chapters=chapters, subject=subject)

@delete_bp.route('/chapter/<int:chapter_id>/topics')
@login_required
def list_topics(chapter_id):
    topics = db.get_topics(chapter_id)
    chapter = db.get_chapter(chapter_id)
    return render_template('delete_list_topics.html', topics=topics, chapter=chapter)

@delete_bp.route('/day/<int:day_id>/times')
@login_required
def list_times(day_id):
    times = db.get_times(day_id)
    day = db.get_day(day_id)

    formatted_times = []
    from datetime import datetime as dt, time as t
    for time_rec in times:
        t_str = dt.combine(dt.today(), t(time_rec[1], time_rec[2])).strftime("%I:%M%p")
        formatted_times.append((time_rec[0], t_str))

    return render_template('delete_list_times.html', times=formatted_times, day=day)
