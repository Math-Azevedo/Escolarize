# usuarios/forms.py
from django import forms
from .models import Usuario, Aluno, Professor, Responsavel, Materia
from notas.models import Disciplina

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'tipo_usuario', 'telefone']
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não conferem")
        return password2

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
    cpf = forms.CharField(
        label='CPF',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'})
    )
    telefone = forms.CharField(
        label='Telefone',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'})
    )
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Responsavel
        fields = ('cpf', 'telefone', 'endereco', 'data_nascimento', 'sexo')