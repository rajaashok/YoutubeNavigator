from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import numpy as np
from enum import Enum


class Action(Enum):
	UNKNOWN = 0
	LEFT = 1
	RIGHT = 2
	CLOSE = 3

def eye_aspect_ratio(eye):
	#print(eye[1], eye[5])
	#print(eye[2], eye[4])
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	#print(A, B , C)
	ear = (A + B) / (2.0 * C)
	return ear

def angle_btn_eyes(leftEyePts, rightEyePts):
	# compute the center of mass for each eye
	leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
	rightEyeCenter = rightEyePts.mean(axis=0).astype("int")
 
	# compute the angle between the eye centroids
	dY = rightEyeCenter[1] - leftEyeCenter[1]
	dX = rightEyeCenter[0] - leftEyeCenter[0]
	angle = np.degrees(np.arctan2(dY, dX))
	return angle



def fetch_action(cap, detect, predict):
	thresh = 0.25
	tilt_frame_check = 10
	closed_frame_check = 20	
	(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
	(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
	# register flags for left, right and closed actions
	left_flag=0
	right_flag=0
	closed_flag=0
	# Set action to unknown
	rec_action = Action.UNKNOWN
	while True:
		ret, frame=cap.read()
		frame = imutils.resize(frame, width=200)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		subjects = detect(gray, 0)
		for subject in subjects:
			shape = predict(gray, subject)
			shape = face_utils.shape_to_np(shape)#converting to NumPy Array			
			leftEye = shape[lStart:lEnd]
			rightEye = shape[rStart:rEnd]
			# Calculate angle between eyes
			angle_between_eyes = angle_btn_eyes(leftEye, rightEye)
			# Calculate Eye Aspect Ratio
			leftEAR = eye_aspect_ratio(leftEye)
			rightEAR = eye_aspect_ratio(rightEye)
			ear = (leftEAR + rightEAR) / 2.0
			
			#print(angle_between_eyes, ear, thresh, ear<thresh)
			if angle_between_eyes <= -130 and angle_between_eyes >= -175 :
				left_flag += 1
				if left_flag >= tilt_frame_check:
					rec_action = Action.LEFT 
					return rec_action
			elif angle_between_eyes >= 130 and angle_between_eyes <= 160 :
				right_flag += 1
				if right_flag >= tilt_frame_check:
					rec_action = Action.RIGHT 
					return rec_action
			elif ear < thresh:
				closed_flag += 1
				if closed_flag >= closed_frame_check:
					rec_action = Action.CLOSE 
					return rec_action
			else:
				flag = 0
	return rec_action

def highlight(element):
    """Highlights a Selenium webdriver element"""
    driver = element._parent
    style = "border: 4px solid red"
    driver.execute_script("arguments[0].setAttribute('style', arguments[1])", element, style)

def un_highlight(element, orignal_style):
    """Highlights a Selenium webdriver element"""
    driver = element._parent
    driver.execute_script("arguments[0].setAttribute('style', arguments[1])", element, orignal_style)


cap=cv2.VideoCapture(0)
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


chrome_options = Options()
chrome_options.add_argument("--disable-user-media-security=true")
# Enable the kiost option for full screen mode
#chrome_options.add_argument("--kiosk")


# Point chromedriver to the location of the chrome driver executable
chromedriver = "chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)

driver.get("http://www.youtube.com")

# Define search queries
queries = ["lionel messi", "never stand still by dan schulman","dhoni world cup final", "steve jobs", "chennai super kings"]
search_xpath = '//*[@id="search"]'
#elem = driver.find_element_by_id("search")
elem = driver.find_elements(By.XPATH, search_xpath)[1]

# Start with index zero and action as UNKNWOWN. Iterate through the list based on left/right tilt 
index = 0
total_values = len(queries)

action_ = Action.UNKNOWN
highlight(elem)
elem.send_keys(queries[index])
# Sleep to setup Screen recording 
time.sleep(20)

while action_ != Action.CLOSE:
	action_ = fetch_action(cap, detect, predict)
	if action_ == Action.LEFT:
		index -= 1
		if index < 0: 
			index = total_values + index
		elem.clear()
		elem.send_keys(queries[index])
	elif action_ == Action.RIGHT:
		index += 1
		if index >= total_values: 
			index = 0
		elem.clear()
		elem.send_keys(queries[index])
	time.sleep(1)

#elem.send_keys(query)
elem.send_keys(Keys.RETURN)


links_xpath = '//*[@id="video-title"]'

RESULTS_LOCATOR = '''//*[@id="contents"]/ytd-video-renderer'''
WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))

page1_results = driver.find_elements(By.XPATH, RESULTS_LOCATOR)
links = []

# Fetch the first link and highlight the selection
sel_element = page1_results[0]
sel_element_orig_style  = sel_element.get_attribute('style')
highlight(sel_element)

total_values = len(page1_results)
action_ = Action.UNKNOWN
index = 0
scroll_height = 1000

while action_ != Action.CLOSE:
	action_ = fetch_action(cap, detect, predict)
	if action_ == Action.LEFT:
		index -= 1
		if index < 0: 
			index = total_values + index
		
	elif action_ == Action.RIGHT:
		index += 1
		if index >= total_values: 
			index = 0
	
	un_highlight(sel_element, sel_element_orig_style)
	sel_element = page1_results[index]
	sel_element_orig_style  = sel_element.get_attribute('style')
	highlight(sel_element)
	scroll_height = scroll_height * (index/3)
	#sel_element.location_once_scrolled_into_view
	#Scroll the page to navigate to the highlighted search result
	driver.execute_script("arguments[0].scrollIntoView();", sel_element)
	driver.execute_script("window.scrollBy(0, -150);")
	time.sleep(1)


# Click the selected item
sel_element.click()

# Wait for CLOSED EYES to pause the video
action_ = Action.UNKNOWN
while action_ != Action.CLOSE:
	action_ = fetch_action(cap, detect, predict)
	driver.find_elements(By.XPATH, '''//*[@id="player"]''')[0].click()


time.sleep(2)
# Wait for CLOSED EYES to play the video
action_ = Action.UNKNOWN
while action_ != Action.CLOSE:
	action_ = fetch_action(cap, detect, predict)
	driver.find_elements(By.XPATH, '''//*[@id="player"]''')[0].click()


time.sleep(60)
driver.quit()
cv2.destroyAllWindows()
cap.release()



#driver.close()