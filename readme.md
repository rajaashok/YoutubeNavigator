## YouTube Navigator
This code can help browse through YouTube with the help of facial alignment

## Applications
This technology can be used to browse Netflix, YouTube, and other streaming services. This technology could be added to an Operating System to browse through PC


### Code Requirements
The example code is in Python ([version 2.7](https://www.python.org/download/releases/2.7/) or higher will work). 

### Dependencies

1) import cv2
2) import immutils
3) import dlib
4) import scipy
5) import selenium
6) import Enum


### Algorithm

Each eye is represented by 6 (x, y)-coordinates, starting at the left-corner of the eye (as if you were looking at the person), and then working clockwise around the eye:.

<img src="https://github.com/rajaashok/YoutubeNavigator/blob/master/eye1.jpg">

#### Entity Aspect Ratio

<img src="https://github.com/rajaashok/YoutubeNavigator/blob/master/eye2.png">

#### Face Alignment - Angle between eyes
Measure the centroid of the eyes and measure the angle between the points to calculate the angle of face

<img src="https://github.com/rajaashok/YoutubeNavigator/blob/master/alignment.png">

For more information,
1) [Face ALignment](https://www.pyimagesearch.com/2017/05/22/face-alignment-with-opencv-and-python/)
2) [EAR](https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/)

### Working Example

[![IMAGE ALT TEXT](http://img.youtube.com/vi/_xpUlCTfYao/0.jpg)](http://www.youtube.com/watch?v=_xpUlCTfYao "YouTubeNavigator")

<div align="center">
  <a href="https://www.youtube.com/watch?v=_xpUlCTfYao"><img src="https://www.youtube.com/watch?v=_xpUlCTfYao" alt="YouTubeNavigator"></a>
</div>


### Execution
Clone the project and create a virtual environment from Python Virtual Environment package 

```
> virtualenv venv
```

Activate the environment 

```
> venv\Scripts\activate
```

Install the project requirements

```
(venv) C:\...\..> pip install -r requirements.txt
```


Execute the python script using the command below:

```
<venv> C:\...\..> python YouTubeNavigator.py
```

## END 
