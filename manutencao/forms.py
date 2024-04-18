from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.widgets import DateInput

from .models import Aquario, Manutencao, Especime, Populacao, Notas


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # Retorna o modelo de usuário atual
        fields = ('email', 'first_name', 'last_name')  # Incluindo o campo de grupo

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Se um grupo foi selecionado, adiciona o usuário a esse grupo
            group = self.cleaned_data.get('group')
            if group:
                user.groups.add(group)
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()  # Retorna o modelo de usuário atual
        fields = ('email', 'is_active', 'is_staff', 'is_superuser', 'first_name',
                  'last_name')  # Inclua outros campos necessários aqui


class AquarioForm(forms.ModelForm):
    class Meta:
        model = Aquario
        fields = ['nome', 'tipo', 'volume', 'data_montagem', 'observacao', 'foto']
        widgets = {
            'data_montagem': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'rows': 3, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(AquarioForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})


class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['data', 'tipo_manutencao', 'ph', 'temperatura', 'observacao']
        widgets = {
            'data': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 15})
        }

    def __init__(self, *args, **kwargs):
        super(ManutencaoForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})


class NotasForm(forms.ModelForm):
    class Meta:
        model = Notas
        fields = ['data', 'titulo', 'texto']
        widgets = {
            'data': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(NotasForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})


class EspecimeForm(forms.ModelForm):
    class Meta:
        model = Especime
        fields = ['tipo_especime', 'nome_popular', 'nome_cientifico', 'observacao', 'imagem']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(EspecimeForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})


class PopulacaoForm(forms.ModelForm):
    class Meta:
        model = Populacao
        fields = ['especime', 'quantidade', 'observacao']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super(PopulacaoForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
