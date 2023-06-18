from imageai.Detection import ObjectDetection
import os

def identify_objects(image_path, output_path, model_path="models/yolo.h5"):
    # Initialize the object detection model
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    # Perform object detection and save the image with bounding boxes
    detections = detector.detectObjectsFromImage(input_image=image_path, output_image_path=output_path)

    # Print detected objects and their bounding box coordinates
    print("Detected objects:")
    for detection in detections:
        print(f"{detection['name']} : {detection['percentage_probability']}% at {detection['box_points']}")

    return detections

if __name__ == "__main__":
    input_image = "path/to/input/image.jpg"
    output_image = "path/to/output/image.jpg"
    model_path = "path/to/pretrained/model.h5"  # If you have a custom pretrained model, supply its path here
    identify_objects(input_image, output_image, model_path)