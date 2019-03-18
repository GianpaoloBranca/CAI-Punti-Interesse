from django.forms.widgets import Textarea

class CountableWidget(Textarea):
    template_name = 'widgets/CountableTextArea.html'
