from django.shortcuts import render,redirect
from .forms import HeartParametersForm
from .forms import RegistrationForm
from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np
from django.contrib.auth import login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import BMICalculatorForm
import time


#Creating the prediction view
# users/views.py
def predict(request):
    if request.method == 'POST':
        form = HeartParametersForm(request.POST)
        if form.is_valid():
            # Get the form data
            # Extract and clean all form input fields
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            chest_pain = form.cleaned_data['chest_pain']
            resting_bp = form.cleaned_data['resting_bp']
            cholesterol = form.cleaned_data['cholesterol']
            fasting_bs = form.cleaned_data['fasting_bs']
            resting_ecg = form.cleaned_data['resting_ecg']
            max_heart_rate = form.cleaned_data['max_heart_rate']
            exercise_agina = form.cleaned_data['exercise_agina']
            oldpeak = form.cleaned_data['oldpeak']
            st_slope = form.cleaned_data['st_slope']

            

            # Load the pre-trained Logistic Regression model
            #with open('detecapp/Heart_failure_prediction_model.pkl', 'rb') as model_file:
                #model = pickle.load(model_file)
            model = joblib.load('detecapp/Heart_failure_prediction_model.pkl')    

            # Prepare the data for prediction (convert to the format expected by the model)
            # Prepare the data for prediction (convert to the format expected by the model)
            data=np.array([age,resting_bp,cholesterol,max_heart_rate,oldpeak,sex, chest_pain,fasting_bs, resting_ecg,exercise_agina, st_slope])
# Reshape the array to 2D array
            data_reshaped = data.reshape(1, -1)  # or data.reshape(-1, 1) depending on the specific requirements

           # Ddata = [age, sex, chest_pain, resting_bp, cholesterol, fasting_bs, resting_ecg, max_heart_rate, exercise_agina, oldpeak, st_slope]
            # You need to match the input format used when training the model
            new_data=list(map(float,data))
            # Make the prediction
            prediction = model.predict(data_reshaped)

            # Display the result to the user
            return render(request, 'prediction_result.html', {'prediction': prediction[0]})
    else:
        form = HeartParametersForm()
    return render(request, 'prediction_form.html', {'form': form})


#results view
def results(request):
    return render(request,'prediction_result.html')

#registration view



def registration(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        gender = request.POST['gender']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if User.objects.filter(username = username):
            messages.error(request, 'Username Already Exist! Please try another username')
            return render(request, 'register.html') 
        elif User.objects.filter(email = email):
            messages.error(request, 'Email Already Registered!')
            return render(request, 'register.html')
        elif len(username) > 10:
            messages.error(request, 'Username must not exceed 10 characters')
        elif password and password != password2:
            messages.error(request, "passwords didn't match.Try again")
            return render(request, 'register.html') 
        elif not username.isalnum():
            messages.error(request, 'Username must be Alpha-Numeric')
            return render(request, 'register.html') 

        def create_user(username, email, fname = None, lname=None):
            user = User(username=username, email=email, fname=fname, lname=lname)
            user.save()
        #myuser = User.objects.create_user(fname, lname, gender, username, email, password, password2)
        #myuser.save()
        messages.success(request, 'Your account has been created successfully')
        return redirect('signin')    
    return render(request, 'register.html')  

def signin(request):
     if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
             login(request, user)
             return redirect('prediction_form')
        else:
            messages.error(request, 'Credentials do not Match, Check your name and password again or go to register.')
            return redirect('signin')

     return render(request, 'signin.html')

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request, 'about.html')
def signout(request):
    logout(request)
    messages.success(request, 'You have successfully Logged out')
    return redirect('home')


def bmi_calculator(request):
     if request.method == 'POST':
        form = BMICalculatorForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            bmi = calculate_bmi(weight, height)
            roundedbmi = np.around(bmi, 2)
            category = get_bmi_category(roundedbmi)
            suggestions = get_suggestions(category)
            return render(request, 'bmi_results.html', {'roundedbmi': roundedbmi, 'category': category, 'suggestions': suggestions})
     else:
        form = BMICalculatorForm()
     return render(request, 'bmi_calculator.html', {'form': form})

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"
    
def bmi_results(request):
    return render(request, 'bmi_results.html')


def get_suggestions(category):
    if category == "Underweight":
        suggestions = """
        - Ensure you're eating enough calories to meet your body's needs. Consider adding calorie-dense foods to your meals, such as:
          - Avocado: Add slices of avocado to your salads or sandwiches.
          - Nut butters: Spread peanut butter or almond butter on toast or fruits.
          - Olive oil: Use olive oil as a dressing or for cooking to increase calorie intake.

        - Focus on nutrient-dense foods. Include a variety of nutrient-rich options in your meals, such as:
          - Lean proteins: Include sources like chicken breast, fish, tofu, or legumes.
          - Whole grains: Opt for whole wheat bread, brown rice, quinoa, or oats.
          - Dairy or dairy alternatives: Choose low-fat milk, yogurt, or plant-based milk fortified with calcium.

        - Include healthy fats in your diet. Incorporate sources of healthy fats, such as:
          - Nuts and seeds: Snack on almonds, walnuts, chia seeds, or flaxseeds.
          - Fatty fish: Include salmon, sardines, or trout in your diet for omega-3 fatty acids.
          - Avocado: Add avocado slices to salads, sandwiches, or smoothies.

        - Consider consulting a healthcare professional or nutritionist for personalized advice. They can assess your specific needs and provide tailored recommendations based on your health status, activity level, and dietary preferences.
        """
    elif category == "Normal":
        suggestions = """
        - Maintain a balanced diet with a variety of foods. Include the following in your meals:
          - Fruits and vegetables: Aim for a colorful assortment of fruits and vegetables daily.
          - Lean proteins: Include sources like chicken, turkey, fish, tofu, eggs, or legumes.
          - Whole grains: Opt for whole wheat bread, brown rice, quinoa, or oats.
          - Dairy or dairy alternatives: Choose low-fat milk, yogurt, or plant-based milk fortified with calcium.

        - Stay physically active and incorporate exercise into your routine. Engage in activities you enjoy, such as brisk walking, cycling, swimming, or dancing.

        - Continue to monitor your weight and make healthy choices. Maintain a balanced energy intake and output to support a healthy weight.
        """
    elif category == "Overweight":
        suggestions = """
        - Focus on portion control and mindful eating. Be mindful of your serving sizes and listen to your body's hunger and fullness cues.

        - Incorporate more fruits and vegetables into your diet. Fill half of your plate with colorful fruits and vegetables for added fiber and nutrients.

        - Reduce your intake of sugary and processed foods. Limit your consumption of sugary beverages, candies, pastries, and processed snacks.

        - Increase your physical activity level. Aim for at least 150 minutes of moderate-intensity aerobic activity per week, such as brisk walking, jogging, or cycling.

        - Consult a healthcare professional or nutritionist for personalized advice. They can provide guidance on creating a balanced meal plan and developing healthy habits for weight management.
        """
    elif category == "Obese":
        suggestions = """
        - Consider adopting a well-balanced, portion-controlled diet. Focus on consuming a variety of nutrient-rich foods in appropriate portions.

        - Incorporate regular exercise into your routine. Engage in activities that you enjoy and aim for a combination of cardiovascular exercise and strength training.

        - Set realistic weight loss goals. Gradual and sustainable weight loss is recommended for long-term success.

        - Seek guidance from a healthcare professional or nutritionist. They can provide personalized advice and support throughout your weight loss journey.

        - Stay motivated and consistent in your efforts. Surround yourself with a supportive environment and make positive lifestyle changes for lasting results.
        """
    else:
        suggestions = "None"
    
    return suggestions