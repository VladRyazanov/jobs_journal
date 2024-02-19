from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    team_leader = IntegerField("id руководителя", validators=[DataRequired()])
    job = StringField("Название работы", validators=[DataRequired()])
    work_size = IntegerField("Объем работы в часах", validators=[DataRequired()])
    collaborators = StringField("id участников через запятую", validators=[DataRequired()])
    start_date = DateField("Дата начала")
    end_date = DateField("Дата окончания")
    is_finished = BooleanField("Завершена")
    submit = SubmitField('Добавить')
