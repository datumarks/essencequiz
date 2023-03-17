from flask import Flask, render_template, request
import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import io
import base64
import os


app = Flask(__name__)

# Load the model
with open('xgb.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the quiz questions
with open('questions.txt', 'r') as f:
    questions = [line.strip() for line in f.readlines()]

# Define the reverse brand archetypes dictionary
reverse_brand_archetypes = {
    1: "Royal",
    2: "Creator",
    3: "Nurturer",
    4: "Entertainer",
    5: "Lover",
    6: "Citizen",
    7: "Maverick",
    8: "Magician",
    9: "Hero",
    10: "Sage",
    11: "Explorer",
    0: "Innocent"
}

# Define the answer key dictionary
answer_key = {"A": 1, "B": 2, None: 0}


# #Connect to the database
# mydb = pymysql.connect(
#   host="localhost",
#   user="datuhdad_creator",
#   password="Wisdom_Extraction321!",
#   database="datuhdad_essence_extraction_db"
# )


#directs to home page of quiz
@app.route('/')
def index():
    return render_template('quiz.html', questions=questions)

@app.route('/process_quiz', methods=['POST'])
def process_quiz():
    # Get the user's answers
    taker_answers = [request.form.get(f'question{i+1}') for i in range(len(questions))]
    
    # Get the user's name and email
    name = request.form['name']
    email = request.form['email']

    # Convert the answers to a numpy array
    output_list = [answer_key.get(item) for item in taker_answers]
    output_list = np.array(output_list).reshape(1, 31)
    
    # Get the model prediction
    pred = model.predict(output_list)[0]
    
    # Get the model prediction probabilities
    probas = model.predict_proba(output_list)

    # Get the second and third highest prediction for each sample
    second_preds = np.argsort(probas, axis=1)[:, -2]
    third_preds = np.argsort(probas, axis=1)[:, -3]
    
    # Get the archetypes
    player_archetype = reverse_brand_archetypes[int(pred)]
    player_archetype2 = reverse_brand_archetypes[int(second_preds)]
    player_archetype3 = reverse_brand_archetypes[int(third_preds)]
    
    # Get the probabilities of each archetype
    first_prob = probas[0][int(pred)]
    second_prob = probas[0][int(second_preds)]
    third_prob = probas[0][int(third_preds)]
    
    # Define the data for the chart
    labels = [f'{player_archetype}', f'{player_archetype2}', f'{player_archetype3}']
    values = [first_prob, second_prob, third_prob] # normalized values that sum up to 1

    # Set the colors for the bars
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    # Create the figure and axis objects
    fig, ax = plt.subplots()

    # Plot the bars
    ax.bar(labels, values, color=colors)

    # Set the y-axis limits to show the full range of values (0-1)
    ax.set_ylim([0, 1])

    # Add labels to the bars
    for i, v in enumerate(values):
        ax.text(i, v/2, '{:.0%}'.format(v), color='white', ha='center', va='center')

    # Add a title and labels for the axes
    ax.set_title("Breakdown of a Brand's Archetype")
    ax.set_xlabel('TOP 3 Archetypes')
    ax.set_ylabel('Normalized Value')

    # Save the chart to a bytes object
    bytes_obj = io.BytesIO()
    plt.savefig(bytes_obj, format='png')
    bytes_obj.seek(0)

    # Encode the bytes as a base64 string for embedding in HTML
    b64_chart = base64.b64encode(bytes_obj.read()).decode('utf-8')





    # cursor = mydb.cursor()
    # sql = "INSERT INTO quiz_results (name, email, results, player_archetype, player_archetype2, player_archetype3, taker_answers) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # val = (name, email, str(probas), player_archetype, player_archetype2, player_archetype3, str(taker_answers))
    # try:
    #     cursor.execute(sql, val)
    #     mydb.commit()
    # except Exception as e:
    #     mydb.rollback()
    #     return f"An error occurred: {e}"
    # mydb.close()



    # Display the chart and quiz results in the HTML template
    return render_template('results.html', name=name, email=email, archetype=player_archetype, chart=b64_chart, probas=str(probas), taker_answers=str(taker_answers))

    
        # # Display the chart in the HTML template
        # return render_template('results.html', name=name, email=email, archetype=player_archetype, chart=b64_chart)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)






