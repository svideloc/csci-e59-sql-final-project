CREATE TABLE `DATASETS` (
  `dataset_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(20) NOT NULL,
  `type` VARCHAR(20) NOT NULL,
  `description` VARCHAR(100) NOT NULL
);

CREATE TABLE `IMAGES` (
  `image_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `dataset_id` INT NOT NULL,
  `type` VARCHAR(20) NOT NULL,
  `description` VARCHAR(20) NOT NULL,
  FOREIGN KEY (`dataset_id`) REFERENCES `DATASETS`(`dataset_id`)
);

CREATE TABLE `MODELS` (
  `model_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `key` VARCHAR(20) NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `description` VARCHAR(100) NOT NULL
);

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
  FOREIGN KEY (`model_id`) REFERENCES `DATASETS`(`dataset_id`)
);

CREATE TABLE `RESULTS_METADATA` (
  `results_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `evaluation_id` INT NOT NULL,
  `precision` DECIMAL(5,2) NOT NULL,
  `recall` DECIMAL(5,2) NOT NULL,
  `true_pos` DECIMAL(5,2) NOT NULL,
  `false_pos` DECIMAL(5,2) NOT NULL,
  `false_neg` DECIMAL(5,2) NOT NULL,
  `probability` DECIMAL(5,2) NOT NULL,
  `image_id` INT NOT NULL,
  FOREIGN KEY (`image_id`) REFERENCES `IMAGES`(`image_id`),
  FOREIGN KEY (`evaluation_id`) REFERENCES `EVALUATION`(`evaluation_id`)
);

CREATE TABLE `TRUTH_LABELS` (
  `truth_label_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `image_id` INT NOT NULL,
  `xmin` DECIMAL(8,3) NOT NULL,
  `xmax` DECIMAL(8,3) NOT NULL,
  `ymin` DECIMAL(8,3) NOT NULL,
  `ymax` DECIMAL(8,3) NOT NULL,
  `class` VARCHAR(20) NOT NULL,
  FOREIGN KEY (`image_id`) REFERENCES `IMAGES`(`image_id`)
);

CREATE TABLE `DETECTIONS` (
  `detection_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `model_id` INT NOT NULL,
  `image_id` INT NOT NULL,
  `xmin` DECIMAL(8,3) NOT NULL,
  `xmax` DECIMAL(8,3) NOT NULL,
  `ymin` DECIMAL(8,3) NOT NULL,
  `ymax` DECIMAL(8,3) NOT NULL,
  `predicted_calss` VARCHAR(20) NOT NULL,
  `probability` DECIMAL(5,2) NOT NULL,
  FOREIGN KEY (`model_id`) REFERENCES `MODELS`(`model_id`),
  FOREIGN KEY (`model_id`) REFERENCES `IMAGES`(`image_id`)
);
