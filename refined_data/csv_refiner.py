import csv

FIELDS = [
    "year",
    "vote_intention",
    "region",
    "province",
    "gender",
    "age",
    "age_cats",
    "degree",
    "language",
]

input_file = "VoteIntentionsDatabase.csv"
output_file = "RefinedVoteIntentionsDatabase.csv"

with open(input_file, newline="", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=FIELDS)

    writer.writeheader()

    for row in reader:
        if int(row["year"]) <= 1999:
            continue

        if any(row[field].strip() == "" for field in FIELDS):
            continue

        writer.writerow({field: row[field] for field in FIELDS})