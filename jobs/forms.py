from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile
from .models import Job
from .models import Application


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True
    )

    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role'
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        if commit:

            user.save()

            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )

        return user


class JobForm(forms.ModelForm):

    class Meta:

        model = Job

        fields = [
            'title',
            'company',
            'location',
            'category',
            'description',
            'requirements',
            'salary',
            'job_type'
        ]

        widgets = {

            'description':
                forms.Textarea(attrs={
                    'rows': 6
                }),

            'requirements':
                forms.Textarea(attrs={
                    'rows': 6
                }),
        }


class ApplicationForm(forms.ModelForm):

    class Meta:

        model = Application

        fields = [
            'resume',
            'cover_letter'
        ]

        widgets = {

            'cover_letter':
                forms.Textarea(attrs={
                    'rows': 6
                })
        }

    def clean_resume(self):

        resume = self.cleaned_data['resume']

        allowed = (
            '.pdf',
            '.doc',
            '.docx'
        )

        if not resume.name.lower().endswith(allowed):

            raise forms.ValidationError(
                'Only PDF, DOC and DOCX files are allowed.'
            )

        if resume.size > 5 * 1024 * 1024:

            raise forms.ValidationError(
                'Resume must be less than 5 MB.'
            )

        return resume


class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            'phone',
            'location',
            'bio',
            'company_name'
        ]

        widgets = {

            'bio':
                forms.Textarea(attrs={
                    'rows': 5
                })
        }