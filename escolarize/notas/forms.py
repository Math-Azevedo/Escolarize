# notas/forms.py
from django import forms
from .models import Serie, Materia, Nota

class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['nome', 'ano_letivo', 'professores']
        widgets = {
            'professores': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['nome', 'ano_letivo']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nome', 'carga_horaria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['nota']
        widgets = {
            'nota': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '10'
            })
        }

    def clean_nota(self):
        nota = self.cleaned_data['nota']
        if nota < 0 or nota > 10:
            raise forms.ValidationError('A nota deve estar entre 0 e 10.')
        return nota