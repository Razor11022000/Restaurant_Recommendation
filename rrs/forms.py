from django import forms


class NameForm(forms.Form):
    sentence = forms.CharField(max_length=100)
    cuisine = forms.ChoiceField(
        choices=[('Mexican', 'Mexican'), ('Indian', 'Indian'), ('Bars', 'Bars'), ('American (New)', 'American (New)'), ('Italian', 'Italian'), ('none', 'none')])
    city = forms.ChoiceField(
        choices=[('Philadelphia', 'Philadelphia'), ('Nashville', 'Nashville'), ('New Orleans', 'New Orleans')])
