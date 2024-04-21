# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.preprocessing import LabelEncoder



# Load the dataset (replace 'cars.csv' with the actual path to your dataset)
data = pd.read_csv('HeartDiseaseTrainTest.csv')

label_encoder = LabelEncoder()
data['sex_enc'] = label_encoder.fit_transform(data['sex'])
data['Chest_pain_type_enc'] = label_encoder.fit_transform(data['chest_pain_type'])
data['fasting_blood_sugar_enc'] = label_encoder.fit_transform(data['fasting_blood_sugar'])
data['rest_ecg_enc'] = label_encoder.fit_transform(data['rest_ecg'])
data['exercise_induced_angina_enc'] = label_encoder.fit_transform(data['exercise_induced_angina'])
data['slope_enc'] = label_encoder.fit_transform(data['slope'])

data=data.drop(['sex','slope','rest_ecg','exercise_induced_angina','fasting_blood_sugar','chest_pain_type'],axis=1)
# Assuming you have a target column called 'is_fast' and feature columns
X = data.drop(columns=['target'])  # Features
y = data['target']  # Target variable

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# Create and train a Logistic Regression model
my_model = LogisticRegression()
my_model.fit(X_train, y_train)

# Evaluate the model (you can add more evaluation code here if needed)


# Save the trained model as a .pkl file
joblib.dump(my_model, 'Heart_failure_prediction_model.pkl')

