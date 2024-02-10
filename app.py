import streamlit as st
import pandas as pd
import pickle


with open('voting_classifier.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

def recommend_crop(pH, phosphorus, potassium, urea, temperature):
    try:
        pH = float(pH)
        phosphorus = int(phosphorus)
        potassium = int(potassium)
        urea = int(urea)
        temperature = float(temperature)
        

        pH_mean, pH_std = 6.311596, 0.424663 
        phosphorus_mean, phosphorus_std = 23.479479, 8.756160 
        potassium_mean, potassium_std = 146.067966, 47.294006 
        urea_mean, urea_std = 52.474345, 20.965486  
        temperature_mean, temperature_std = 72.532048,8.950912  
        
        pH_normalized = (pH - pH_mean) / pH_std
        phosphorus_normalized = (phosphorus - phosphorus_mean) / phosphorus_std
        potassium_normalized = (potassium - potassium_mean) / potassium_std
        urea_normalized = (urea - urea_mean) / urea_std
        temperature_normalized = (temperature - temperature_mean) / temperature_std
        
        input_data = pd.DataFrame({
            'pH': [pH_normalized],
            'Phosphorus': [phosphorus_normalized],
            'Potassium': [potassium_normalized],
            'Urea': [urea_normalized],
            'Temperature': [temperature_normalized]
        })
        prediction = model.predict(input_data)[0]
        return prediction
    except ValueError:
        return None

st.title('Crop Recommendation System')

st.markdown(
    """
    <style>
    /* Title */
    .title h1 {
         color: #333333;
        background-color: #f0f0f0;
        padding: 10px 20px; /* Adjusted padding */
        border-radius: 10px;
        text-align: center;
        font-size: 12px; /* Decreased font size */
        margin-bottom: 20px;
        margin-top: 20px; /* Added margin-top */
    }

    /* Form Header */
    .form-header {
        font-size: 24px;
        color: #006600;
        margin-bottom: 20px;
    }

    /* Input Fields */
    .input-field {
        border: 2px solid #999999;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 15px;
        width: 100%;
        font-size: 18px;
    }

    /* Submit Button */
    .submit-button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 30px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 20px;
        margin-top: 20px;
        border-radius: 25px; /* Rounded corners */
        cursor: pointer;
        transition: background-color 0.3s; /* Smooth transition for hover effect */
    }

    .submit-button:hover {
        background-color: #45a049; /* Darker shade of green on hover */
    }

    /* Success Message */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
    }
</style>

    """,
    unsafe_allow_html=True
)

st.header('Input Parameters')
pH = st.text_input('pH')
phosphorus = st.text_input('Phosphorus')
potassium = st.text_input('Potassium')
urea = st.text_input('Urea')
temperature = st.text_input('Temperature')

submitted = st.button('Recommend')

if submitted:
    try:
      
        pH = float(pH)
        phosphorus = float(phosphorus)
        potassium = float(potassium)
        urea = float(urea)
        temperature = float(temperature)

        recommended_crop = recommend_crop(pH, phosphorus, potassium, urea, temperature)
        if recommended_crop is not None:
            st.success(f'Recommended Crop: {recommended_crop}')
        else:
            st.error("Please enter valid numerical values for all input parameters.")
    except ValueError:
        st.error("Please enter valid numerical values for all input parameters.")
