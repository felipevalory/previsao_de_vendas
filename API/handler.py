import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann_project import Rossmann

# Loading model
model = pickle.load(open('C:/Users/Felipe/Documents/Felipe/Cursos/'
                         'CientistaDados/repos/ds_production/'
                         'rossmann_project/model/'
                         'model_xgb_tuned_rossmann.pkl', 'rb'))

# Initialize API
app = Flask(__name__)


@app.route('/rossmann/predict', methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()

    if test_json:

        if isinstance(test_json, dict):  # Unique exemple

            test_raw = pd.DataFrame(test_json, index=[0])

        else:  # multiple exemples

            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())

        # Instantiate Rossmann Class
        pipeline = Rossmann()

        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)

        # feature engineering
        df2 = pipeline.feature_engineering(df1)

        # data preparation
        df3 = pipeline.data_preparation(df2)

        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)

        return df_response

    else:
        return Response('{}', status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run('0.0.0.0')
