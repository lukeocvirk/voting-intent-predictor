# Vote Intent Predictor
This project encompasses a model used to predict voting patterns for Canadian federal elections based on demographic data.

# How to train the model:
The data for this project was accessed at:
https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP3/2EUFYD

To train the model, start by downloading and extracting this dataset, then move "VoteIntentionsDatabase.csv" into the refined_data folder.
After this, run the following commands to execute the data refinement script:
`cd refined_data`
`python csv_refiner.py` (or `python3 csv_refiner.py` on macOS)