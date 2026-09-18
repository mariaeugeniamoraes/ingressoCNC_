"""
Formulários do site.

Aqui ficam as validações de cadastro e de edição de perfil.
Colocar as regras no formulário (e não na view) evita repetir código
e faz o Django mostrar as mensagens de erro no campo certo.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CadastroForm(UserCreationForm):
    """Cadastro com e-mail obrigatório e sem repetir e-mail já usado."""

    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "voce@exemplo.com"}),
    )

    first_name = forms.CharField(
        required=False,
        max_length=30,
        label="Nome",
    )

    last_name = forms.CharField(
        required=False,
        max_length=150,
        label="Sobrenome",
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

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
    """Edição dos dados pessoais: nome, sobrenome e e-mail."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
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
        O e-mail continua único, mas sem reclamar do e-mail
        que já pertence à própria pessoa.
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