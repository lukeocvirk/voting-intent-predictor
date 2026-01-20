# Vote Intent Predictor
This project encompasses a model used to predict voting patterns for Canadian federal elections based on demographic data.

# How to train the model:
The data for this project was accessed at:
https://borealisdata.ca/dataset.xhtml?persistentId=doi:10.5683/SP3/2EUFYD

To train the model, start by downloading and extracting this dataset, then move "VoteIntentionsDatabase.csv" into the refined_data folder.
After this, run the following commands to execute the data refinement script:
`cd refined_data`
`python3 csv_refiner.py` (or `python csv_refiner.py` if not running on macOS)

Next, run these commands to train the model (it will take some time):
`cd ../model`
`python3 model.py`

Next, you can sample the model based on any set of attributes you want to include. This script generates N (recommend 100) synthetic voters based on your criteria which is converted into an estimated % chance of voting for a particular party based on your given attributes.

The attributes included in the model's training data are: year (2023 is recommended; otherwise undefined behaviour), region, province, gender, age_cats, degree, language. For a breakdown of these attributes and what their possible values are, read the codebook in `canadian_vote_intention_dataset/VoteIntentionDatabase/Document/Vote_Intention_Codebook_and_TD.pdf`.

To run the sampling script use the following format:
`python3 sampling.py --year 2023 --province 35 --gender 0 --age_cats 1 --degree 0 --language 2 --n 100 --show-samples`
The above example represents a male voter from Ontario, within the 18-29 age range, with a university education and with English as the primary language spoken at home.

Below is a breakdown of the included attributes and their values (from the codebook):

region
o (1) Atlantic
o (2) Quebec
o (3) Ontario
o (4) Prairies
o (5) British Columbia
o (6) North

province
o (10) Newfoundland and Labrador
o (11) Prince Edward Island
o (12) Nova Scotia
o (13) New Brunswick
o (24) Quebec
o (35) Ontario
o (46) Manitoba
o (47) Saskatchewan
o (48) Alberta
o (59) British Columbia
o (60) Yukon
o (61) Northwest Territories
o (62) Nunavut

gender
o (0) Man
o (1) Woman
o (2) Non-binary / Other gender identity

age_cats
o (1) 18-29
o (2) 30-49
o (3) 50+

degree
o (0) No university degree.
o (1) University education (bachelor’s degree or above).

language
o (1) “French”
o (2) “English”
o (4) “Other”