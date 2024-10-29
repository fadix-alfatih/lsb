from django import forms
from django.contrib.auth.forms import UsernameField
from django.forms import FileInput

from lsb.models import Penyisipan, Ekstraksi

class FormSignIn(forms.Form):
    username = UsernameField(
    	widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
    	widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class FormDaftar(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'email',
                'placeholder': 'Email'
                }
            )
        )
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
                'placeholder': 'Username'
                }
            )
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'name': 'password',
                 'placeholder': 'Password'
                }
            )
        )
    passwordconf = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 
                'name': 'password',
                 'placeholder': 'Konfirmasi Password'
                }
            )
        )

class FormPenyisipan(forms.ModelForm):
    pesan = forms.CharField(
        label='Pesan Rahasia',
        max_length=1000,
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Pesan Rahasia'
                }
            )
        )
    class Meta:
        model = Penyisipan
        fields = ['gambar',]
        widgets = {
            'gambar':FileInput(attrs={
                'class':'form-control',
                'onchange':'previewImage(event)',
                })
        }
        

class FormEkstraksi(forms.ModelForm):
    class Meta:
        model = Ekstraksi
        fields = ['gambar',]
        widgets = {
            'gambar':FileInput(attrs={
                'class':'form-control',
                'onchange':'previewImage(event)',
                })
        }