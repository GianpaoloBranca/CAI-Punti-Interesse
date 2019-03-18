from django.forms.widgets import Textarea, Input

class CountableTextArea(Textarea):
    template_name = 'custom_widgets/CountableTextArea.html'

    class Media:
        js = ('custom_widgets/CountableTextArea.js',)

class ImageInput(Input):
    template_name = 'custom_widgets/ImageInput.html'
