# usuarios/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import Usuario, Aluno, Professor, Responsavel, Materia
from notas.models import Materia, Serie, Disciplina
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_professor']
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

class AlunoUsuarioForm(forms.ModelForm):

    class Meta:
        model = Aluno
        fields = ['nome', 'idade', 'serie', 'materias']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control'}),
            'serie': forms.Select(attrs={'class': 'form-control'}),
            'materias': forms.SelectMultiple(attrs={'class': 'form-control'}),

        }

    # Tente importar o modelo 'Serie' aqui de forma tardia
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['identificador', 'formacao', 'materias']
        widgets = {
            'identificador': forms.TextInput(attrs={'class': 'form-control'}),
            'formacao': forms.TextInput(attrs={'class': 'form-control'}),
            'series': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'materias': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['materias'].queryset = Materia.objects.all()

    def save(self, commit=True):
        professor = super().save(commit=False)
        if commit:
            professor.save()
            self.save_m2m()  # Salva os relacionamentos many-to-many
        return professor

class ResponsavelForm(forms.ModelForm):
    matricula_aluno = forms.CharField(
        label="Matrícula do Aluno", 
        max_length=20, 
        required=True, 
        help_text="Insira a matrícula do aluno para associar o responsável."
    )

    class Meta:
        model = Responsavel
        fields = ['identificador', 'nome', 'data_nascimento', 'cpf', 'sexo', 'endereco']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def clean_matricula_aluno(self):
        matricula = self.cleaned_data.get('matricula_aluno')
        try:
            aluno = Aluno.objects.get(identificador=matricula)  # alterado para 'identificador'
        except Aluno.DoesNotExist:
            raise forms.ValidationError("Aluno com esta matrícula não foi encontrado.")
        return matricula


    def save(self, commit=True):
        responsavel = super().save(commit=False)
        matricula_aluno = self.cleaned_data['matricula_aluno']
        
        # Buscar a instância do aluno correspondente à matrícula
        aluno = get_object_or_404(Aluno, identificador=matricula_aluno)
        
        # Atribuir a instância do aluno ao campo 'aluno' do responsável
        responsavel.aluno = aluno
        
        if commit:
            responsavel.save()
        return responsavel
