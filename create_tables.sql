CREATE TABLE `DATASETS` (
  `dataset_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(20) NOT NULL,
  `type` VARCHAR(20) NOT NULL,
  `description` VARCHAR(100) NOT NULL
);

CREATE TABLE `IMAGES` (
  `image_id` VARCHAR(20) NOT NULL PRIMARY KEY,
  `dataset_id` INT NOT NULL,
  FOREIGN KEY (`dataset_id`) REFERENCES `DATASETS`(`dataset_id`)
);

CREATE TABLE `MODELS` (
  `model_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `type` VARCHAR(20) NOT NULL,
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
  FOREIGN KEY (`dataset_id`) REFERENCES `DATASETS`(`dataset_id`)
);

CREATE TABLE `RESULTS_METADATA` (
  `results_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `evaluation_id` INT NOT NULL,
  `prec` DECIMAL(8,3) NOT NULL,
  `rec` DECIMAL(8,3) NOT NULL,
  `true_pos` INT NOT NULL,
  `false_pos` INT NOT NULL,
  `false_neg` INT NOT NULL,
  `prob` DECIMAL(8,3) NOT NULL,
  FOREIGN KEY (`evaluation_id`) REFERENCES `EVALUATION`(`evaluation_id`)
);

CREATE TABLE `TRUTH_LABELS` (
  `truth_label_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `image_id` VARCHAR(20) NOT NULL,
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
  `image_id` VARCHAR(20) NOT NULL,
  `xmin` DECIMAL(8,3) NOT NULL,
  `xmax` DECIMAL(8,3) NOT NULL,
  `ymin` DECIMAL(8,3) NOT NULL,
  `ymax` DECIMAL(8,3) NOT NULL,
  `predicted_class` VARCHAR(20) NOT NULL,
  `probability` DECIMAL(5,2) NOT NULL,
  FOREIGN KEY (`model_id`) REFERENCES `MODELS`(`model_id`),
  FOREIGN KEY (`image_id`) REFERENCES `IMAGES`(`image_id`)
);

