# parking_lot
To determine the number of available spaces to park a vehicle from a given image of a parking lot.

## Creating a Parking Map
The file map.csv can be created by the python script in map_creator folder. 
* **USE:** python map_creator.py
```
This opens up a GUI which you can use to mark the spaces which are parking lots. This map can also be automatically generated using object trackers and dwell time. We will integrate that part with this code soon.
```

## Preparing the Object Detector
You can run the light weight object detector by downloading the pretrained weights for mobile ssd. 
* **URL:** https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

```
Place the frozen_inference_graph.pb file for MobileSSD trained on COCO Dataset in the models folder.
```

## Getting the Results!
* **USE:** python3 main.py src/img/input.jpg dst/img/output.jpg
```
The output in the terminal shows the number of available parking slots by matching the processed image map and the map created by the user using the GUI. The operation takes the average area of bounding boxes of the vehicles to do so. 
```
