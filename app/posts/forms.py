from wtforms import Form, StringField, TextAreaField, validators

class PostForm(Form):
    title = StringField(u'Title', [validators.DataRequired(), validators.Length(min=3)])
    content = TextAreaField(u'Content')