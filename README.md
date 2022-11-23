# face-recognition-assignment

This is the given task or assignment for the role of data science intern at absolute face

## Requirements

- Python 3.6
- OpenCV 3.3.0 or above
- Numpy 1.14.3 or above


## Installation
```
    pip3 install opencv-python --default-timeout=10009
    pip3 install opencv-contrib-python --default-timeout=10009
    pip3 install numpy pillow openpyxl pandas tabulate
```

## Run

1. Collect datasets for a person.
   ```
   python3 face_datasets.py -n "Ravishanker"
   ```
   Change the name for different persons, it will generate unique id for each face and names.json will be generated.

2. Train the datasets
    ```
    python3 training.py
    ```
3. Recognize facces
    ```
    python3 face_recognition.py
    ```
4. To cleanup
    ```
    python3 cleanup.py
    ```
