# usuarios/forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario, Aluno, Professor, Responsavel, Materia
from notas.models import Disciplina
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }


        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não conferem")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Por favor, preencha ambos os campos de senha")
        return cleaned_data

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['matricula', 'data_nascimento', 'serie', 'responsavel','password']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['identificador', 'formacao', 'series', 'materias']
        widgets = {
            'series': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'materias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Garante que todas as matérias estarão disponíveis no campo de seleção
        self.fields['materias'].queryset = Disciplina.objects.all()

    def save(self, commit=True):
        professor = super().save(commit=False)
        if commit:
            professor.save()
            self.save_m2m()  # Salva os relacionamentos many-to-many
        return professor

class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ['cpf', 'telefone', 'endereco', 'data_nascimento', 'sexo']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)