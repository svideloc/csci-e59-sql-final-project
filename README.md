# mySQL Database for Automated Target Recognition (ATR) Common Evaulation Store

Final Project for Designing and Developing Relational and NoSQL Databases (CSCI E59)

[Link to Presentation](https://www.canva.com/design/DAE-WG1qk5A/iOBoycNkYgKFXwu4GECifw/view?utm_content=DAE-WG1qk5A&utm_campaign=designshare&utm_medium=link&utm_source=publishpresent)

## Problem Statement

**Design database for storing data relevant to the detection and evaluation of Automated Target Recognition (ATR) models.**

The client requires that the system that can leverage "Gold" datasets to evaluate models from different teams to determine which model is performing best on a common evaluation process.

Data such as what model was used, what dateset was used, truth labels, detections, and image metadata will all need to be stored in a place that can be easily queried, in order to show common evaluation metrics such as Precision/Recall tables for a given model run and identify models that are performing best on a particular dataset.

## mySQL Design

See the below diagram to understand the structure of the dataset.

![diagram](images/diagram2.png)

I chose a sql database because of the many foreign key interactions, and likely transactions that will be going on to the database at the same time. Multiple users will be able to access the WEB UI at any given moment, meaning that multiple evalations can be run with any number of models/datasets. Having this organized into the tables in the design above will prove to be useful as the project scales with more models and datasets.

Let's go through each table, its purpose, and what data it is storing.

### MODELS & DATASETS

*MODELS* and *DATASETS* are two of the simpler tables in the dataset. The *MODELS* table simply captures each model that is available in the evaluation. Similarly the *DATASETS* table shows which datasets are available to inference the evaluation against. Users looking at the UI, will likely see a list of available models and datasets which will be derived from these tables!See the below `SELECT` statement for the kind of data that exists in these two tables:

```
mysql> SELECT * FROM MODELS LIMIT 5;
+----------+-------------+------+----------------------------+
| model_id | type        | name | description                |
+----------+-------------+------+----------------------------+
|        1 | retinaBoats | boat | retina net model for boats |
|        2 | fasterBoats | boat | faster rcnn for boats      |
|        3 | fasterCats  | cats | faster rcnn for cats       |
|        4 | fasterCats  | dogs | faster rcnn for dogs       |
+----------+-------------+------+----------------------------+
4 rows in set (0.00 sec)

mysql> SELECT * FROM MODELS LIMIT 4;
+----------+-------------+------+----------------------------+
| model_id | type        | name | description                |
+----------+-------------+------+----------------------------+
|        1 | retinaBoats | boat | retina net model for boats |
|        2 | fasterBoats | boat | faster rcnn for boats      |
|        3 | fasterCats  | cats | faster rcnn for cats       |
|        4 | fasterCats  | dogs | faster rcnn for dogs       |
+----------+-------------+------+----------------------------+
4 rows in set (0.00 sec)
```

### IMAGES

*IMAGES* really just refers to the image metadata, for the class example I'm just going to use the `image_id` (which will just be the name of the file for now) and a **FOREIGN KEY** reference to the `dataset_id` from the *DATASETS* table for which an image belongs in. You will notice in the diagram a one to many relationship as one image can actually belong in multiple datasets! See the below image for the kind of data that exists in this table:

```
mysql> SELECT * FROM IMAGES LIMIT 5;
+-----------+------------+
| image_id  | dataset_id |
+-----------+------------+
| 00aa8bc42 |          1 |
| 00c3e1386 |          1 |
| 00c54cf6e |          1 |
| 00ce2c1c0 |          1 |
| 0a09da25f |          1 |
+-----------+------------+
5 rows in set (0.00 sec)
```

### DETECTIONS and TRUTH_LABELS

These two tables show where actual objects are in an image. The *TRUTH_LABELS* table obviously shows where the true objects are in a particular `image_id` (**FOREIGN KEY** reference to the *IMAGES* table). The data you will find will be the `xmin`, `xmax`, `ymin`, `ymax` of where an object is in an image and of course what that object is. The *DETECTIONS* Table is very similar, but it is what the model predicted on an image (**FOREIGN KEY** reference to the *MODELS* table). See the below `SELECT` statement for the kind of data that exists in these two tables:

```
mysql> SELECT * FROM TRUTH_LABELS LIMIT 5;
+----------------+-----------+---------+---------+---------+---------+-------+
| truth_label_id | image_id  | xmin    | xmax    | ymin    | ymax    | class |
+----------------+-----------+---------+---------+---------+---------+-------+
|              1 | 0a09da25f | 506.000 | 627.000 |  26.000 |  87.000 | boat  |
|              2 | 0a15f8996 | 532.000 | 710.000 |   4.000 |  60.000 | boat  |
|              3 | ff890d001 |  21.000 | 202.000 | 448.000 | 540.000 | boat  |
|              4 | 0b652af9e | 429.000 | 543.000 | 518.000 | 616.000 | boat  |
|              5 | ffc00cde1 | 447.000 | 768.000 | 153.000 | 252.000 | boat  |
+----------------+-----------+---------+---------+---------+---------+-------+
5 rows in set (0.00 sec)
```

### EVALUATION

The *EVALUATION* table is a great summary table for how a model performed. It will tell you which model and dataset was used, the time of the evaluation, and the score of the model as well as some other associated metadata. This will be a simple table to query for users looking at the UI, wanting to compare different model runs. See below for the type of data in this table:

```
mysql> SELECT * FROM EVALUATION LIMIT 5;
+---------------+----------+------------+---------------------+--------+-------+----------+------+
| evaluation_id | model_id | dataset_id | timestamp           | object | score | metric   | IOU  |
+---------------+----------+------------+---------------------+--------+-------+----------+------+
|             1 |        1 |          1 | 2022-04-23 01:37:17 | boat   |  0.94 | AP_SCORE | 0.50 |
|             2 |        1 |          1 | 2022-04-24 18:53:55 | boat   |  0.96 | AP_SCORE | 0.30 |
|             3 |        2 |          1 | 2022-04-24 19:16:29 | boat   |  0.99 | AP_SCORE | 0.50 |
|             4 |        2 |          1 | 2022-04-24 19:16:50 | boat   |  1.00 | AP_SCORE | 0.30 |
|             5 |        4 |          2 | 2022-04-24 19:37:06 | dog    |  0.90 | AP_SCORE | 0.50 |
+---------------+----------+------------+---------------------+--------+-------+----------+------+
5 rows in set (0.00 sec)
```

### RESULTS_METADATA

This table contians the metadata that determined the score in the *EVALUATION* table. It is very useful to view this data ordered by probability of a detection, to view how the precision and recall scores change as our threshold/probability goes down. See below for the type of data that exists in this table:

```
mysql> SELECT * FROM RESULTS_METADATA LIMIT 5;
+------------+---------------+-------+-------+----------+-----------+-----------+-------+
| results_id | evaluation_id | prec  | rec   | true_pos | false_pos | false_neg | prob  |
+------------+---------------+-------+-------+----------+-----------+-----------+-------+
|          1 |             1 | 1.000 | 0.010 |        1 |         0 |       106 | 0.999 |
|          2 |             1 | 1.000 | 0.020 |        2 |         0 |       105 | 0.997 |
|          3 |             1 | 1.000 | 0.030 |        3 |         0 |       104 | 0.996 |
|          4 |             1 | 1.000 | 0.040 |        4 |         0 |       103 | 0.996 |
|          5 |             1 | 1.000 | 0.050 |        5 |         0 |       102 | 0.996 |
+------------+---------------+-------+-------+----------+-----------+-----------+-------+
5 rows in set (0.00 sec)
```

## Creating Database & Tables

The database was created with the following command:

```sql
CREATE DATABASE atr_eval;
```

View the databse:

```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| atr_eval           |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.21 sec)
```

Use the new database:

```sql
mysql> use atr_eval;
```

See the file [create_tables.sql](create_tables.sql) file for the sql code for creating the tables. Here is an example of creating a table for the *EVALUATION* table:

```sql
CREATE TABLE `EVALUATION` (
  `evaluation_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `model_id` INT NOT NULL,
  `dataset_id` INT NOT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `object` VARCHAR(20) NOT NULL,
  `score` DECIMAL(5,2) NOT NULL,
  `metric` VARCHAR(20) NOT NULL,
  `IOU` DECIMAL(3,2) NOT NULL,
  FOREIGN KEY (`model_id`) REFERENCES `MODELS`(`model_id`),
  FOREIGN KEY (`dataset_id`) REFERENCES `DATASETS`(`dataset_id`)
);
```

Show all of the tables:

```
mysql> show tables;
+--------------------+
| Tables_in_atr_eval |
+--------------------+
| DATASETS           |
| DETECTIONS         |
| EVALUATION         |
| IMAGES             |
| MODELS             |
| RESULTS_METADATA   |
| TRUTH_LABELS       |
+--------------------+
7 rows in set (0.01 sec)
```

## Inserting Data (with Python)

See the file [insert_data.py](insert_data.py) for the python code to insert code efficiently into the mySQL database for my data. Below is quick example of how to use the `mysql.connector` library in python for inserting the image data into the *IMAGES* table for an example.

```py
# import needed libraries
import os
import mysql.connector

# func to get sql query and data
def get_images_metadata(location, dataset_id):

    # read in data
    files = os.listdir(location)
    image_names = [os.path.splitext(f)[0] for f in files]

    # convert to list of tuples
    data = [os.path.splittext(f)[0] for f in image_names]

    # create sql statement
    sql = "INSERT INTO IMAGES (dataset_id, image_id) VALUES (%s, %s)"

    return sql, data

# connect to database
mydb = mysql.connector.connect(host="localhost", user="root",
            password="MYPASSWORD", database="atr_eval")
mycursor = mydb.cursor()

# get sql statemetn and associated metadata
sql, data = get_images_metadata(args.data_path, args.dataset_id)

# insert rows
mycursor.executemany(sql, data)
mydb.commit()
print(mycursor.rowcount, "was inserted.")
```

## Common Queries
