import os
import sys
import argparse
from pathlib import Path
import mysql.connector

import pandas as pd

DESC = """
Insert data into SQL DB

Example
-------
python insert_data.py --actions DATASETS --typeorkey boat --description "gold dataset for boats" --name retinaBoats --password PASSWORD

python insert_data.py --actions MODELS --typeorkey boat --description "retina net model for boats" --name retinaBoats --password PASSWORD

python insert_data.py --actions EVALUATION --model-id 1 --dataset-id 1 --object boat --score 0.94 --metric AP_SCORE --iou 0.5 --password PASSWORD

python insert_data.py --actions IMAGES --data-path /home/svidelock/harvard_extension/csciE59/project/data/model1/detections --dataset-id 1 --password PASSWORD

python insert_data.py --actions DETECTIONS --data-path /home/svidelock/harvard_extension/csciE59/project/data/model1/detections --model-id 1 --password PASSWORD

python insert_data.py --actions TRUTH_LABELS --data-path /home/svidelock/harvard_extension/csciE59/project/data/model1/ground_truth --password PASSWORD

python insert_data.py --actions RESULTS_METADATA --data-path /home/svidelock/harvard_extension/csciE59/project/data/model1/resultsIOU=0.50/all_results.csv --evaluation-id 1 --password PASSWORD
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
    default="root"
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
    "--name",
    help="name of dataset"
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

# func for inserting into datasets table
def add_dataset(name, typee, description):

    # create tuple
    data = (name, typee, description)

    # create query
    sql = "INSERT INTO DATASETS (name, type, description) VALUES (%s, %s, %s)"

    return sql, data

# func for inserting into models table
def add_models(name, typee, description):

    # create tuple
    data = (name, typee, description)

    # create query
    sql = "INSERT INTO MODELS (name, type, description) VALUES (%s, %s, %s)"

    return sql, data

# func for inserting into evaluation table
def add_evaluation(model_id, dataset_id, objectt, score, metric, iou):

    # create tuple
    data = (model_id, dataset_id, objectt, score, metric, iou)

    # create query
    sql = "INSERT INTO EVALUATION (model_id, dataset_id, object, score, metric, IOU) VALUES (%s, %s, %s, %s, %s, %s)"

    return sql, data

# fun for inserting into images table
def get_images_metadata(location, dataset_id):

    # read in data
    files = os.listdir(location)
    image_names = [os.path.splitext(f)[0] for f in files]

    # convert to list of tuples
    data = []
    for img in image_names:
        data.append((dataset_id, img))

    # create sql statement
    sql = "INSERT INTO IMAGES (dataset_id, image_id) VALUES (%s, %s)"

    return sql, data

# func for inserting into detections table
def get_detections(location, model_id):

    # read in data
    files = os.listdir(location)
    full_paths = [os.path.join(location, f) for f in files]

    # convert to list of tuples, same order as below
    data = []
    for detections in full_paths:
        df = pd.read_csv(detections, names=['object', 'prob', 'xmin', 'ymin', 'xmax', 'ymax'], delimiter=" ")
        for iterr, row in df.iterrows():
            tuple_data = (model_id, Path(detections).stem, row.xmin, row.xmax, row.ymin, row.ymax, row.object, row.prob)
            data.append(tuple_data)

    # create sql statement
    sql = "INSERT INTO DETECTIONS (model_id, image_id, xmin, xmax, ymin, ymax, predicted_class, probability) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    return sql, data

# func for inserting into ground truths table
def get_ground_truths(location):

    # read in data
    files = os.listdir(location)
    full_paths = [os.path.join(location, f) for f in files]

    # convert to list of tuples, same order as below
    data = []
    for detections in full_paths:
        df = pd.read_csv(detections, names=['object', 'xmin', 'ymin', 'xmax', 'ymax'], delimiter=" ")
        for iterr, row in df.iterrows():
            tuple_data = (Path(detections).stem, row.xmin, row.xmax, row.ymin, row.ymax, row.object)
            data.append(tuple_data)

    # create sql statement
    sql = "INSERT INTO TRUTH_LABELS (image_id, xmin, xmax, ymin, ymax, class) VALUES (%s, %s, %s, %s, %s, %s)"

    return sql, data

# func for inserting into results_metadata table
def get_results_metadata(location, evaluation_id):

    # read in data
    df = pd.read_csv(location)

    # convert to list of tuples
    data = []
    for iterr, row in df.iterrows():
        tuple_data = (evaluation_id, float(row.precision), float(row.recall), int(row.acc_TP), int(row.acc_FP), int(row.acc_FN), float(row.threshold))
        data.append(tuple_data)

    # create sql statement
    sql = "INSERT INTO RESULTS_METADATA (evaluation_id, prec, rec, true_pos, false_pos, false_neg, prob) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    return sql, data


if __name__ == "__main__":

    args = parser.parse_args()

    # setup connection to db
    mydb = mysql.connector.connect(
        host="localhost",
        user=args.user,
        password=args.password,
        database="atr_eval"
    )

    mycursor = mydb.cursor()

    if args.actions == "DATASETS":
        sql, data = add_dataset(args.name, args.typeorkey, args.description)

    if args.actions == "MODELS":
        sql, data = add_models(args.typeorkey, args.name, args.description)

    if args.actions == "EVALUATION":
        sql, data = add_evaluation(args.model_id, args.dataset_id, args.object, args.score, args.metric, args.iou)

    if args.actions == "IMAGES":
        sql, data = get_images_metadata(args.data_path, args.dataset_id)

    if args.actions == "DETECTIONS":
        sql, data = get_detections(args.data_path, args.model_id)

    if args.actions == "TRUTH_LABELS":
        sql, data = get_ground_truths(args.data_path)

    if args.actions == "RESULTS_METADATA":
        sql, data = get_results_metadata(args.data_path, args.evaluation_id)

    if args.actions in ["DATASETS", "EVALUATION", "MODELS"]:
        mycursor.execute(sql, data)
    else:
        mycursor.executemany(sql, data)

    mydb.commit()
    print(mycursor.rowcount, "was inserted.")
