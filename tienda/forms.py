from django import  forms
from .models import Cliente, Compras

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'cedula', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control campo', 'placeholder': 'Nombre'}),
            'correo': forms.EmailInput(attrs={'class':'form-control campo', 'placeholder': 'Correo'}),
            'cedula': forms.TextInput(attrs={'class':'form-control campo', 'placeholder': 'Cédula'}),
            'telefono': forms.TextInput(attrs={'class':'form-control campo', 'placeholder': 'Teléfono'}),
            'direccion': forms.TextInput(attrs={'class':'form-control campo', 'placeholder': 'Dirección'}),
        }
        def clean_cedula(self):
            cedula = self.cleaned_data.get('cedula')
            if len(cedula) != 10:
                raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")
            return cedula

        def clean_telefono(self):
            telefono = self.cleaned_data.get('telefono')
            if len(telefono) < 10:
                raise forms.ValidationError("El teléfono debe tener al menos 10 dígitos.")
            return telefono

class ComprasForm(forms.ModelForm):
    class Meta:
        model = Compras
        fields = ['productos', 'comprador', 'precio_final']  
        widgets = {
            'productos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'comprador': forms.Select(attrs={'class': 'form-control'}),
            'precio_final': forms.NumberInput(attrs={'class': 'form-control'}),
        }