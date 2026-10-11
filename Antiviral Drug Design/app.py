import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import difflib
import pickle

with open('clf.pkl', 'rb') as f:
    clf = pickle.load(f)
with open('features.pkl', 'rb') as f:
    selected_features = pickle.load(f)
scaler = joblib.load('scaler.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
label_encoder_source = joblib.load('label_encoder_source.pkl')
label_encoder_family = joblib.load('label_encoder_family.pkl')
label_encoder_target = joblib.load('label_encoder_target.pkl')

df = pd.read_csv('dataset.csv')

def preprocess_sequence(sequence):
    X_sequence_tfidf = tfidf_vectorizer.transform([sequence])
    return X_sequence_tfidf.toarray()

def get_closest_match(sequence, df):
    closest_match = difflib.get_close_matches(sequence, df['Sequence'], n=1)
    if closest_match:
        closest_sequence = closest_match[0]
        return df[df['Sequence'] == closest_sequence]
    else:
        return None

def preprocess_input_data(input_data, closest_match_df):
    closest_sequence_data = closest_match_df.iloc[0]
    
    input_data['Sequence_Length'] = len(input_data['Sequence'])
    input_data['pI'] = closest_sequence_data['pI']
    input_data['Basic_residues'] = closest_sequence_data['Basic_residues']
    input_data['Acidic_residues'] = closest_sequence_data['Acidic_residues']
    input_data['Net_charge'] = closest_sequence_data['Net_charge']
    input_data['Polar_residues'] = closest_sequence_data['Polar_residues']
    input_data['Hydrophobic_residues'] = closest_sequence_data['Hydrophobic_residues']
    input_data['Hydrophobicity'] = closest_sequence_data['Hydrophobicity']
    input_data['Boman_Index'] = closest_sequence_data['Boman_Index']
    input_data['Aliphatic_Index'] = closest_sequence_data['Aliphatic_Index']
    input_data['Extinction_Coefficient_cystines'] = closest_sequence_data['Extinction_Coefficient_cystines']
    
    source_encoded = label_encoder_source.transform([input_data['Source']])
    family_encoded = label_encoder_family.transform([input_data['Family']])
    
    input_data_df = pd.DataFrame([input_data])
    
    input_data_df['Source_encoded'] = source_encoded
    input_data_df['Family_encoded'] = family_encoded
    
    input_data_df.drop(columns=['Source', 'Family'], inplace=True)
    
    X_sequence_scaled = preprocess_sequence(input_data['Sequence'])
    X_sequence_df = pd.DataFrame(X_sequence_scaled, columns=tfidf_vectorizer.get_feature_names_out())
    
    input_data_df = pd.concat([input_data_df, X_sequence_df], axis=1)
    
    numeric_columns = ['Sequence_Length', 'pI', 'Basic_residues', 'Acidic_residues', 
                       'Net_charge', 'Polar_residues', 'Hydrophobic_residues', 'Hydrophobicity',
                       'Boman_Index', 'Aliphatic_Index', 'Extinction_Coefficient_cystines']
    
    input_data_df[numeric_columns] = scaler.transform(input_data_df[numeric_columns])
    input_data_df.drop(columns=['Sequence'], inplace=True)
    selected_data = input_data_df.iloc[:, selected_features]
    
    return selected_data

st.title('AntiViral Drug Classification')
st.write("Enter a peptide sequence to get the classification prediction.")

sequence_input = st.text_input("Peptide Sequence")
source_input = st.text_input("Source Organism")
family_input = st.text_input("Family")

if sequence_input and source_input and family_input:
    input_data = {
        'Sequence': sequence_input,
        'Source': source_input,
        'Family': family_input
    }
    if st.button("Check Anti-Virality"):
        closest_match_df = get_closest_match(sequence_input, df)
        if closest_match_df is not None:
            selected_data = preprocess_input_data(input_data, closest_match_df)
            
            prediction_prob = clf.predict_proba(selected_data)
            
            target_names = label_encoder_target.classes_
            predicted_class = target_names[np.argmax(prediction_prob)]
            probability = np.max(prediction_prob)
            
            st.write(f"Predicted Target: {predicted_class}")
            st.write(f"Prediction Probability: {probability * 100:.2f}%")
        else:
            st.write("No matching sequence found in the dataset.")
