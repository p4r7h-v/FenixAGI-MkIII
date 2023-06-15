import numpy as np
import tensorflow as tf
import cv2
from PIL import Image
from urllib.request import urlretrieve

def download_model():
    url = "http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz"
    model_file = "ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz"
    urlretrieve(url, model_file)
    return model_file

def extract_model(model_file):
    import tarfile
    tar = tarfile.open(model_file, "r:gz")
    tar.extractall()
    tar.close()

def load_model():
    model_dir = "ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model"
    return tf.saved_model.load(str(model_dir))

def load_labels():
    label_file = "https://raw.githubusercontent.com/tensorflow/models/master/research/object_detection/data/mscoco_label_map.pbtxt"
    class_names = ['???']
    with open(label_file) as f:
        for line in f.readlines():
            if "display_name" in line:
                class_names.append(line.split(":")[-1].strip().replace('"', ''))
    return class_names

def identify_objects(image_path, model, class_names):
    def preprocess_image(image):
        input_tensor = tf.convert_to_tensor(image)
        input_tensor = input_tensor[tf.newaxis, ...]
        return input_tensor

    def get_objects_info(detections):
        objects_info = []
        for i in range(int(detections.pop('num_detections'))):
            class_id = int(detections['detection_classes'][0][i].numpy())
            class_name = class_names[class_id]
            score = detections['detection_scores'][0][i].numpy()
            bbox_raw = detections['detection_boxes'][0][i].numpy()

            objects_info.append({
                "class_id": class_id,
                "class_name": class_name,
                "score": score,
                "bbox_raw": bbox_raw
            })
        return objects_info

    img = Image.open(image_path)
    img = np.asarray(img)
    preprocessed_image = preprocess_image(img)
    detections = model(preprocessed_image)
    objects_info = get_objects_info(detections)

    return objects_info