from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
import re
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r'[A-Z]', password):
        errors.append("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', password):
        errors.append("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r'[^a-zA-Z0-9]', password):
        errors.append("La contraseña debe contener al menos un carácter especial.")
    if re.search(r'(?:012|123|234|345|456|567|678|789|890)', password):
        errors.append("No se permiten números consecutivos en la contraseña.")
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    lowered = password.lower()
    for i in range(len(lowered) - 2):
        if lowered[i:i+3] in alphabet:
            errors.append("No se permiten letras consecutivas en la contraseña.")
            break
    return errors

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
    
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if errors := validate_password(password):
            raise forms.ValidationError(errors)
        return password

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario/Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Usuario o email'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Tu contraseña'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                return CustomUser.objects.get(email=username).username
            except CustomUser.DoesNotExist:
                pass
        return username

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'bio', 'avatar')


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistroForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'register-username',
            'placeholder': 'Tu nombre de usuario'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'register-email',
            'placeholder': 'tu@email.com'
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'register-password',
            'placeholder': 'Crea una contraseña segura'
        })
    )
    password2 = forms.CharField(
                label="Confirmar Contraseña",
                strip=False,
                widget=forms.PasswordInput(attrs={
                    'class': 'form-control',
                    'id': 'register-password-confirm',  # antes era register-password2
                    'placeholder': 'Confirma tu contraseña'
            })
        )
    terms = forms.BooleanField(
            label='Acepto',
            widget=forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'terms',   # antes era register-terms
            })
        )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        # Actualizamos widget de username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'register-username',
            'placeholder': 'Tu nombre de usuario'
        })
        # Ajustamos widget de email
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'register-email',
            'placeholder': 'tu@email.com'
        })
        # Ocultamos help_texts por defecto si quieres
        for field in ['username', 'password1', 'password2']:
            if field in self.fields:
                self.fields[field].help_text = None


    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Las contraseñas no coinciden.")
        return cleaned