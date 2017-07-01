# Taxonomy API

API used for predicting the cognitive level of a question

# Training the API
In order for the API to be retrained based on new data, the CSV file in the /data folder needs to be replaced by a newer version.
The right csv file can be retrieved by using the following SQL Query:
```sql
SELECT * FROM
```

# Using the API
## GET /task
Endpoint used for the cognitive level prediction
 
query-string: introduction={introduction}

{introduction}:
The introduction of a question should be converted to a URL encoded string.

