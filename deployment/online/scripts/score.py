import os
import logging
import os
import json
import mlflow
from io import StringIO
import pandas as pd 

from mlflow.pyfunc.scoring_server import infer_and_parse_json_input, predictions_to_json
from azureml.ai.monitoring import Collector


def init():
    """
    This function is called when the container is initialized/started, typically after create/update of the deployment.
    You can write the logic here to perform init operations like caching the model in memory
    """
    global model
    global input_schema
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)

     
    files_path = [os.path.abspath(x) for x in os.listdir(os.getenv("AZUREML_MODEL_DIR"))]
    print(files_path)
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "taxi-model-auto/model.pkl"
    )

    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "taxi-model-auto")
    model = mlflow.pyfunc.load_model(model_path)    
    input_schema = model.metadata.get_input_schema()

    # deserialize the model file back into a sklearn model
    # model = joblib.load(model_path)
    logging.info("Init complete")
    global inputs_collector, outputs_collector
    # inputs_collector = Collector(name='model_inputs')  
    inputs_collector = Collector(name='model_inputs', on_error=lambda e: logging.info("ex:{}".format(e)))        
    outputs_collector = Collector(name='model_outputs')
    # inputs_outputs_collector = Collector(name='model_inputs_outputs')



def run(raw_data):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    logging.info("Request received")
    json_data = json.loads(raw_data)
    if "input_data" not in json_data.keys():
        raise Exception("Request must contain a top level key named 'input_data'")

    serving_input = json.dumps(json_data["input_data"])
    data = infer_and_parse_json_input(serving_input, input_schema)
    predictions = model.predict(data)
    datafr=pd.DataFrame(json_data["input_data"], columns = json_data["columns"] )
    context = inputs_collector.collect(datafr) 
    result = model.predict(data)
    # outputs_collector.collect(result, context)   
    result = StringIO()
    predictions_to_json(predictions, result)
    return result.getvalue()
    
    # data = json.loads(raw_data)["data"]
    # data = numpy.array(data)
    # result = model.predict(data)
    # logging.info("Request processed")
    # context = inputs_collector.collect(data) 
    # result = model.predict(data)
    # outputs_collector.collect(result, context)    
    # return result.tolist()