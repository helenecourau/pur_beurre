from django import forms
import re


class AccountForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="Prénom")
    last_name = forms.CharField(max_length=30, label="Nom")
    username = forms.CharField(max_length=30, label="Nom d'utilisateur")
    mail = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Mot de passe",
                               help_text="Longueur minimale de 12 caractères.",
                               widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data['password']
        test = r"\S{12,}"
        if not re.match(test, password):
            raise forms.ValidationError("Il faut une longueur minimale de 12 caractères!")

        return password


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class SaveForm(forms.Form):
    article_id = forms.IntegerField(label="id")
