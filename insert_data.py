import os
import sys
import argparse
import mysql.connector

import pandas as pd

DESC = """
Insert data into SQL DB

Example
-------
python insert_data.py --actions DATASETS --typeorkey boat --description "gold datset for boats" --pasword PASSWORD

python insert_data.py --actions MODELS --typeorkey boat --description "model to detect boats" --pasword PASSWORD

python insert_data.py --actions IMAGES --data-path path/to/images/dir --dataset-id DATASET-ID --pasword PASSWORD

python insert_data.py --actions EVALUATION --model-id MODEL-ID --dataset-id DATASET-ID --object boat --score 75 --metric AP_SCORE --iou 0.5 --pasword PASSWORD

python insert_data.py --actions TRUTH_LABELS --data-path /path/to/truth/labels --pasword PASSWORD

python insert_data.py --actions DETECTIONS --data-path /path/to/detections --model-id MODEL-ID --pasword PASSWORD

python insert_data.py --actions RESULTS_METADATA --data-path /path/to/results --evaluation_id EVALUATION-ID --pasword PASSWORD
"""

parser = argparse.ArgumentParser(description=DESC)


parser.add_argument(
    "--actions",
    choices=['DETECTIONS', 'DATASETS', "EVALUATION", "IMAGES", "MODELS", "RESULTS_METADATA", "TRUTH_LABELS"],    
    help="which table are we putting data into"
)
parser.add_argument(
    "--user",
    help="username",
    default="svidelock"
)
parser.add_argument(
    "--password",
    help="password to mysql database"
)
parser.add_argument(
    "--data-path",
    help="location to the data being ingested, only used for DETECTIONS, IMAGES, RESULTS-METADATA, TRUTH-LABELS"
)
parser.add_argument(
    "--typeorkey",
    help="descriptor one word"
)
parser.add_argument(
    "--description",
    help="description of data or model"
)
parser.add_argument(
    "--dataset-id",
    help="dataset-id, to be used for IMAGES data add"
)
parser.add_argument(
    "--model-id",
    help="model-id, to be used for DETECTIONS data add"
)
parser.add_argument(
    "--object",
    help="to be used in results for EVALUATION table"
)
parser.add_argument(
    "--score",
    help="to be used in results for EVALUATION table"
)
parser.add_argument(
    "--metric",
    help="to be used in results for EVALUATION table"
)
parser.add_argument(
    "--iou",
    help="to be used in results for EVALUATION table"
)
parser.add_argument(
    "--evaluation-id",
    help="evaluation-id, to be used for RESULTS_METADATA data add"
)
parser.add_argument(
    "--data-path",
    help="location to the data being ingested, only used for DETECTIONS, IMAGES, RESULTS-METADATA, TRUTH-LABELS"
)

# func for inserting into datasets table
def add_dataset(name, typee, description):

    # create tuple
    data = (name, typee, description)

    # create query
    sql = "INSERT INTO DATASETS (name, type, description) VALUES (%s, %s, %s)"

    return sql, data

# func for inserting into models table
def add_models(name, key, description):

    # create tuple
    data = (name, key, description)

    # create query
    sql = "INSERT INTO MODELS (name, key, description) VALUES (%s, %s, %s)"

    return sql, data

# fun for inserting into images table
def get_images_metadata(location, dataset_id):

    # read in data


    # convert to list of tuples
    data = []

    # TODO: REMAKE IMAGES TABLE

    # create sql statement
    sql = "INSERT INTO IMAGES (dataset_id, image_name) VALUES (%s, %s)"

    return sql, data

# func for inserting into evaluation table
def add_evaluation(model_id, dataset_id, objectt, score, metric, iou):

    # create tuple
    data = (model_id, dataset_id, objectt, score, metric, iou)

    # create query
    sql = "INSERT INTO EVALUATION (model_id, dataset_id, object, score, metric, IOU) VALUES (%s, %s, %s, %s, %s, %s)"

    return sql, data

# func for inserting into detections table
def get_detections(location, model_id):

    # read in data

    # convert to list of tuples, same order as below
    data = []

    # create sql statement
    sql = "INSERT INTO DETECTIONS (model_id, image_id, xmin, xmax, ymin, ymax, predicted_class, probability) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    return sql, data

# func for inserting into ground truths table
def get_ground_truths(location):

    # read in data

    # convert to list of tuples
    data = []

    # create sql statement
    sql = "INSERT INTO TRUTH_LABELS (image_id, xmin, xmax, ymin, ymax, class) VALUES (%s, %s, %s, %s, %s, %s)"

    return sql, data

# func for inserting into results_metadata table
def get_results_metadata(location, evaluation_id):

    # read in data

    # convert to list of tuples
    data = []

    # create sql statement
    sql = "INSERT INTO RESULTS_METADATA (evaluation_id, precision, recall, true_pos, false_pos, false_neg, probability, image_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    return sql, data


if __name__ == "__main__":

    args = parser.parse_args()

    # setup connection to db
    mydb = mysql.connector.connect(
        host="localhost",
        user=args.user,
        password=args.password,
        database="atr_evaluation"
    )

    mycursor = mydb.cursor()

    if args.actions == "DETECTIONS":
        sql, data = get_detections(args.data_path)

    if args.actions == "DATASETS":
        sql, data = add_dataset(args.data_path)

    if args.actions == "EVALUATION":
        sql, data = add_evaluation(args.data_path)

    if args.actions == "IMAGES":
        sql, data = get_get_images_metadataimages(args.data_path)

    if args.actions == "MODELS":
        sql, data = add_models(args.data_path)

    if args.actions == "RESULTS_METADATA":
        sql, data = get_results_metadata(args.data_path)

    if args.actions == "TRUTH_LABELS":
        sql, data = get_ground_truths(args.data_path)

    # execute sql query
    mycursor.executemany(sql, data)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
