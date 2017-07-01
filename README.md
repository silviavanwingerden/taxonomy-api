# Taxonomy API

API made with Gunicorn and the Falcon web framework used for predicting the cognitive level of a question. 

## Training the API
In order for the API to be retrained based on new data, the CSV file in the /data folder needs to be replaced by a newer version.
The right csv file can be retrieved by using the following SQL Query:
```sql
SELECT `introduction`,`question_type_id` FROM `tasks` WHERE `introduction` != 0
```
Make sure the csv file has the name: "allquestiontypes.csv"
After importing the csv file into the project, run the following command from the /categorize folder:
```
python trainmodel.py
```
The predictions are now based on the data from the new csv file, it recommended to retrain the API periodically.

## Testing the predictions
In order to find out what percentage of the predictions are predicted right you just have to run 1 command
```
python train.py
```
this prints the accuracy of the predictions in a percentage, this number is influenced every time a new model is trained.

## Using the API
### GET /task
Endpoint used for the cognitive level prediction
 
query-string: ?introduction={introduction}

{introduction}:
The introduction of a question should be converted to a URL encoded string.

