from django import forms
from django.forms import ModelForm
from django.core import validators
from appcontacto.models import T_UGC_ACTUALIZA_ANTECEDENTES


class FormularioLogin(forms.Form):
        RUT = forms.CharField(required=True, widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder': 'RUT (sin puntos)', 'autocomplete':'off', 'type':'number', 'min':999999, 'max':99999999}
            ),
        validators= [validators.MaxLengthValidator(8, message='El RUT supera los carcateres maximo')]
        )

        DV = forms.CharField(required=True, widget=forms.TextInput(
            attrs={'class':'form-control', 'placeholder': 'DV', 'autocomplete':'off', 'type':'text', 'maxlength':1}
            ),
        validators= [validators.MaxLengthValidator(1, message='El digito verificador supera los carcateres maximo')]
        )
        
class FormularioContacto(ModelForm):
    RUT = forms.CharField(required=True)
    DV= forms.CharField(required=True)
    TELEFONO1 = forms.CharField()
    TELEFONO2 = forms.CharField(required=True)
    DIRECCION = forms.CharField(required=True)
    COD_REGION = forms.CharField(required=True)
    COD_COMUNA = forms.CharField(required=True)
    DIRECCION_NUMERO = forms.CharField(required=True)
    CORREO_PARTICULAR = forms.CharField(required=True)
    OBSERVACIONES = forms.CharField(required=False,widget=forms.Textarea(attrs={'maxlength':255}))

    class Meta:
        model = T_UGC_ACTUALIZA_ANTECEDENTES
        fields = ['RUT', 'TELEFONO1', 'TELEFONO2', 'DIRECCION','DIRECCION_NUMERO','CORREO_PARTICULAR','COD_REGION', 'COD_COMUNA', 'OBSERVACIONES']


#class FormSisAccesoFuncional(forms.ModelForm):
    
#    class Meta:
#        model = SIS_ACCESO_FUNCIONAL
#        fields = '__all__'
