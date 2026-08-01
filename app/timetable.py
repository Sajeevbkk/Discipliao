from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from db import db
from random import choices
from datetime import datetime, timedelta, time as time_obj

timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')

@timetable_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    days = db.get_days()

    if request.method == 'POST':
        day_id = request.form.get('day_id')
        if not day_id:
            flash('Please select a day.', 'danger')
            return redirect(url_for('timetable.index'))

        times = db.get_times(day_id)
        if not times:
            flash('No times found for the selected day.', 'warning')
            return redirect(url_for('timetable.index'))

        topics = db.get_active_topics()
        if not topics:
            flash('No active topics found.', 'warning')
            return redirect(url_for('timetable.index'))

        try:
            weights = []
            for topic in topics:
                priority = db.get_subject_priority(topic[0])
                if priority is None:
                    priority = 0
                weights.append(topic[5] + priority)

            selected_topics_raw = choices(
                topics,
                weights=weights,
                k=len(times)
            )

            selected_topic_ids = [topic[0] for topic in selected_topics_raw]
            selected_topics = db.get_selected_topics(selected_topic_ids)

            time_table = []
            for time, topic_data in zip(times, selected_topics):
                start_dt = datetime.combine(datetime.today(), time_obj(time[1], time[2]))
                end_dt = start_dt + timedelta(minutes=25)

                start_str = start_dt.strftime("%I:%M%p")
                end_str = end_dt.strftime("%I:%M%p")

                time_table.append({
                    'time': f"{start_str} - {end_str}",
                    'topic': topic_data[0],
                    'chapter': topic_data[1],
                    'subject': topic_data[2]
                })

            day_name = db.get_day(day_id)[1]
            return render_template('timetable_view.html', day_name=day_name, time_table=time_table)

        except Exception as e:
            flash(f'Error generating time table: {str(e)}', 'danger')
            return redirect(url_for('timetable.index'))

    return render_template('timetable_index.html', days=days)
