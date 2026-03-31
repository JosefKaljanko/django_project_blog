from django import forms

# login:
from django.contrib.auth.forms import AuthenticationForm    #
# registrace:
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ContactForm(forms.Form):
    name = forms.CharField(label="Jméno", max_length=80, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    message = forms.CharField(label="Zpráva", widget=forms.Textarea(attrs={"rows": 5}), required=True)

    # honeypot pole (anti-spam): normalni uzivatel ho nevyplní
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Jméno je příliš krátké...")
        return name

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Spam detekován...")
        return cleaned

    # widgets v fieldu v1

    # name = forms.CharField(
    #     label="Jméno",
    #     max_length=80,
    #     widget = forms.TextInput(attrs={
    #         "class": "input",
    #         "placeholder": "Vaše Jméno",
    #     })
    # )

    # widgets v2
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["name"].widget.attrs["placeholder"] = "Zadejte Jméno"
    #     self.fields["email"].widget.attrs["placeholder"] = "E-mail"
    #     self.fields["message"].widget.attrs["placeholder"] = "Zadejte vaši zprávu"
    #
    #     self.fields["name"].widget.attrs["class"] = "input"
    #     self.fields["email"].widget.attrs["class"] = "input"
    #     self.fields["message"].widget.attrs["class"] = "input"
    #
    #     self.fields["message"].widget.attrs["cols"] = 100
    #     self.fields["message"].widget.attrs["rows"] = 10
    #
    #     # self.fields["message"].widget.type = "textarea"
    #
    #     self.fields["message"].help_text = """<ul>
    #                     <li>Zadejte text vaší zprávy.</li>
    #                     <li>Pište stručně.</li>
    #                     <li>V případě potřeby vás budeme kontaktovat.</li>
    #                     </ul>
    #                     """

    # widget v2.2


    # v3
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            print(name, field)
            # zakladni class pro vsechna pole
            base_class = "field"

            # rozsireni podle typu widgetu
            if isinstance(field.widget, forms.Textarea):
                base_class += " field--textarea"
            else:
                base_class += " field--input"

            # bezpečné přidání (neprepise existujici class)
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " " + base_class).strip()

        # individuální doplňky
        self.fields["name"].widget.attrs.setdefault("placeholder", "Např. Josef")
        self.fields["email"].widget.attrs.setdefault("placeholder", "josef@email.cz")
        self.fields["message"].widget.attrs.setdefault("placeholder", "Napiš mi…")


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)

        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " field field--input").strip()

        self.fields["username"].widget.attrs.setdefault("placeholder", "Uživatelské jméno")
        self.fields["password"].widget.attrs.setdefault("placeholder", "Heslo")


class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", required=True)
    first_name = forms.CharField(label="Křestní Jméno",required=False, max_length=30)
    last_name = forms.CharField(label="Příjmení",required=False, max_length=30)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name","password1", "password2")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # jednotné css classy
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " field field--input").strip()

        self.fields["username"].widget.attrs.setdefault("placeholder", "Vaše uživatelské jméno")
        self.fields["email"].widget.attrs.setdefault("placeholder", "Váš Email")

        # upravy attrs , label přes django:
        # self.fields["password1"].widget.attrs.setdefault("placeholder", "Heslo placeholder")
        # self.fields["password1"].label = "Heslo"
        # self.fields["password2"].label = "Heslo Znovu"

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        # default User model nemá unique email tak hlidáme sami
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Tento email je již použitý...")
        return email