from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Members

class HeartParametersForm(forms.Form):
    #AGES = [i for i in range(1, 101)]
    SEX_CHOICES = [('1', 'Male'), ('0', 'Female')]
    CHEST_PAIN_CHOICES = [
        (3, 'Typical Angina'),
        (1, 'Atypical Angina'),
        (2, 'Non-Anginal Pain'),
        (0, 'Asymptomatic')
    ]
    FASTING_BS_CHOICES = [(0, 'FastingBS > 120 mg/dl'), (1, 'FastingBS <= 120 mg/dl')]
    RESTING_ECG_CHOICES = [
        (1, 'Normal'),
        (2, 'ST-T wave abnormality'),
        (0, 'Left Ventricular Hypertrophy')
    ]
    EXERCISE_AGINA_CHOICES = [(1, 'Yes'), (0, 'No')]
    ST_SLOPE_CHOICES = [(2, 'Upsloping'), (1, 'Flat'), (0, 'Downsloping')]

    age = forms.IntegerField(label='Age (years)')
    sex = forms.ChoiceField(label='Sex', choices=SEX_CHOICES)
    chest_pain = forms.ChoiceField(label='Chest Pain Type', choices=CHEST_PAIN_CHOICES)
    resting_bp = forms.IntegerField(label='Resting Blood Pressure (mm Hg)')
    cholesterol = forms.IntegerField(label='Serum Cholesterol (mm/dl)')
    fasting_bs = forms.ChoiceField(label='Fasting Blood Sugar', choices=FASTING_BS_CHOICES)
    resting_ecg = forms.ChoiceField(label='Resting Electrocardiogram Results', choices=RESTING_ECG_CHOICES)
    max_heart_rate = forms.IntegerField(label='Maximum Heart Rate Achieved')
    exercise_agina = forms.ChoiceField(label='Exercise-Induced Angina', choices=EXERCISE_AGINA_CHOICES)
    oldpeak = forms.DecimalField(label='Oldpeak (ST Depression)')
    st_slope = forms.ChoiceField(label='ST Slope', choices=ST_SLOPE_CHOICES)

# users/forms.py

class RegistrationForm(UserCreationForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    )
    fname = forms.CharField(
        label="fname",
        widget=forms.TextInput(attrs={'placeholder':'First Name'}),
    )
    lname = forms.CharField(
        label="lname",
        widget=forms.TextInput(attrs={'placeholder':'Last Name'}),
    )
    gender = forms.CharField(
        label="gender",
        widget=forms.TextInput(attrs={'placeholder':'gender'}),
    )
    birthdate = forms.CharField(
        label="birthdate",
        widget=forms.DateInput(attrs={'placeholder':'date'}),
    )

    class Meta:
        model = User
        fields = ['username','fname','lname','birthdate','gender', 'email', 'password', 'password2']

    class MembersForm(forms.ModelForm):
        class Meta:
            fields = "__all__"    


class BMICalculatorForm(forms.Form):
    weight = forms.FloatField(label='Weight (kg)')
    height = forms.FloatField(label='Height (m)')
