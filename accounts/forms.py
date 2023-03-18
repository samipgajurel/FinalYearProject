from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile
def clean_unique(form, field, exclude_initial=True,
                 format="The %(field)s %(value)s has already been taken."):
    value = form.cleaned_data.get(field)
    if value:
        qs = form._meta.model._default_manager.filter(**{field:value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qs = qs.exclude(**{field:initial_value})
        if qs.count() > 0:
            raise forms.ValidationError(format % {'field':field, 'value':value})
    return value

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = (
        (Profile.CONSUMER, "Consumer"),
        (Profile.FARMER, "Farmer"),
        (Profile.DEALER, "Dealer")
    )
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')
    phone = PhoneNumberField(help_text='Phone Number')
    role = forms.ChoiceField(choices=ROLE_CHOICES, help_text='Role')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
'email','phone','password1', 'password2','role')


class ProfileForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields = ['first_name', 'last_name','email','phone','picture']

    def clean_email(self):
        return clean_unique(self, 'email')