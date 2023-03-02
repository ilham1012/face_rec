# face_rec
This repo contains code for the development of a smart doorlock device. There are two main parts.
The first one is model development. The second one is the application.

## Face recognition model
The model was developed by using the face_recognition package to detect the face and extract its feature vector.
The dataset was collected from a member of our department. It contains a feature vector and the name of the person as the label.
Several classifier algorithms were trained and optimized using hyperparameter optimization. Then, the best classifier was selected as the final model.


## Doorlock app
The app was built to be deployed in the doorlock device. It consisted of two parts: the smart sensor and the actuator. The smart sensor was built using NVIDIA Jetson Nano with a webcam and a touchscreen display. The actuator was built using nodeMCU and a selenoid actuator.

When a user wants to open the door, the model will detect if the person is allowed. The app will then send a signal to the actuator to open the lock.
The administrator is also able to add a new user. The app will record the new user from several angles by asking them to move their head slightly in certain directions. The app will then extract the feature, add them to the dataset, and retrain the classifier model.
