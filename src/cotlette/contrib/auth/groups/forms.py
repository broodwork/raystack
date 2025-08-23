from cotlette.forms.forms import Form
from cotlette.forms.fields import CharField

class GroupCreateForm(Form):
    name = CharField(label='Название группы', required=True)
    description = CharField(label='Описание', required=False) 