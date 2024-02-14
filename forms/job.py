from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField("id руководителя", validators=[DataRequired()])
    job = StringField("Название работы", validators=[DataRequired()])
    work_size = IntegerField("Объем работы в часах", validators=[DataRequired()])
    collaborators = StringField("id участников через запятую", validators=[DataRequired()])
    start_date = StringField("Дата начала")
    end_date = StringField("Дата окончания")
    is_finished = BooleanField("Завершена", validators=DataRequired())
    submit = SubmitField('Добавить')
