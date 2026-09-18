from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CadastroForm(UserCreationForm):
    """Formulário de cadastro de novos usuários."""

    first_name = forms.CharField(
        label="Nome",
        max_length=150,
        required=True
    )

    last_name = forms.CharField(
        label="Sobrenome",
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "voce@exemplo.com"}
        )
    )

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

    def clean_email(self):
        """Impede duas contas com o mesmo e-mail."""

        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Já existe uma conta cadastrada com este e-mail."
            )

        return email

    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.email = self.cleaned_data["email"]

        if commit:
            usuario.save()

        return usuario


class PerfilForm(forms.ModelForm):
    """Formulário para edição dos dados do usuário."""

    class Meta:
        model = User

        fields = [
            "first_name",
            "last_name",
            "email",
        ]

        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].required = True

    def clean_email(self):
        """
        Impede que o usuário utilize um e-mail
        pertencente a outra conta.
        """

        email = self.cleaned_data["email"].strip().lower()

        em_uso = (
            User.objects
            .filter(email__iexact=email)
            .exclude(pk=self.instance.pk)
            .exists()
        )

        if em_uso:
            raise forms.ValidationError(
                "Este e-mail já está sendo usado por outra conta."
            )

        return email