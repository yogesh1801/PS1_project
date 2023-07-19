import pickle
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__,template_folder='C:/Users/ASUS/Desktop/project_final')

with open("RFmodel.pkl", 'rb') as file:
    RFmodel = pickle.load(file)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        inputs = []
        age = float(request.form["age"])
        inputs.append(age)
        BMI = float(request.form["BMI"])
        inputs.append(BMI)
        children = float(request.form["children"])
        inputs.append(children)
        sex = str(request.form["sex"])
        if sex == "male":
            sex = float(1)
        else:
            sex = float(0)
        inputs.append(sex)
            
        smoker = str(request.form["smoker"])
        if smoker == "yes":
            smoker = float(1)
        else:
            smoker = float(0)
        inputs.append(smoker)
        
        regionsobj = {
            "northwest": 0,
            "northeast": 0,
            "southwest": 0,
            "southeast": 0
        }
        region = str(request.form["region"])
        regionsobj[region] = 1
        inputs.append(float(regionsobj["northwest"]))
        inputs.append(float(regionsobj["northeast"]))
        inputs.append(float(regionsobj["southwest"]))
        inputs.append(float(regionsobj["southeast"]))

        input_array = np.array(inputs).reshape(1, -1)

        # Pass the input array to your model
        predicted_value = RFmodel.predict(input_array)

        # Retrieve the predicted value (assuming a single-element output)
        predicted_value = round(predicted_value[0],2)

        return render_template('index.html', prediction=predicted_value)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()