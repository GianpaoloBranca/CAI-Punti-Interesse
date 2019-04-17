from django.forms.widgets import Textarea

class CountableTextArea(Textarea):
    template_name = 'custom_widgets/CountableTextArea.html'

    class Media:
        js = ('custom_widgets/CountableTextArea.js',)
