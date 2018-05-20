import asyncio
import json
import os
import subprocess
import time
from webbrowser import *
class State_Machine:
    states = ['init', 'p_capture_info', 'p_capture', 'p_save', 'gallery' , 'scroll_right', 'scroll_left']
    def __init__(self):
        self.current_state = 'init'

        # INITIALIZE DECISION TREE HERE
        self.decision_tree = False

        self.main_loop()
        pass

    def capture_images(self):
        cmd = ["./build/examples/openpose/openpose.bin", "--display", "0", "--write_images", "/home/lab246/Desktop/jpg_output",
               "--write_images_format", "jpg", "--hand", "--write_json", "/home/lab246/Desktop/json_output"]
        output = subprocess.Popen(cmd, cwd="/home/lab246/Documents/openpose6/openpose")
        time.sleep(3)
        output.kill()
        return True

    def reset_folders(self):
        os.system("rm *.json /home/lab246/Desktop/json_output")
        os.system("rm *.jpg /home/lab246/Desktop/jpg_output")

    def check_for_human(self):
        keypoint_data_dir_path = "/home/lab246/Desktop/json_output"

        # read from a folder json file and see if there is a human in view.
        while True:
            self.capture_images()
            keypoint_data_files = [f for f in os.listdir(keypoint_data_dir_path) if
                                   os.path.isfile(os.path.join(keypoint_data_dir_path, f))]
            highest = keypoint_data_files[0]
            num = highest.split('_keypoints.json')[0]
            for f in keypoint_data_files:
                new_num = int(f.split('_keypoints.json')[0])
                if new_num > num:
                    num = new_num
                    highest = f
            most_current = highest

            current = json.load("/home/lab246/json_output/"+most_current)
            if len(current['people']) != 0:
                self.reset_folders()
                return True
            else:
                self.reset_folders()
                time.sleep(1)


    def get_gesture(self):
        keypoint_data_dir_path = "/home/lab246/Desktop/json_output"
        while True:
            self.capture_images()
            keypoint_data_files = [f for f in os.listdir(keypoint_data_dir_path) if
                                   os.path.isfile(os.path.join(keypoint_data_dir_path, f))]
            highest = keypoint_data_files[0]
            num = highest.split('_keypoints.json')[0]
            for f in keypoint_data_files:
                new_num = int(f.split('_keypoints.json')[0])
                if new_num > num:
                    num = new_num
                    highest = f
            most_current = highest
            current = json.load("home/lab246/Desktop/json_output/most_current.json")
            if len(current['people']) != 0:
                return 'no_human'
            else:
                #assert NotImplementedError('need to implement decision tree here')
                return 'arms_raised'
                #decision_tree(json)
                # returns number
                # if right number

    def main_loop(self):
        while True:
            self.check_for_human()
            self.p_capture_info()
            pass


    def p_capture_info(self):
        # show the info screen
        open_new("file:///home/lab246/Desktop/openpose_project_UI/photoCaptureInformation.html")
        # wait for hands to be raised
        return_code = ''
        while return_code is not 'no_human':
            return_code = self.get_gesture()
            if return_code is 'arms_raised':
                self.p_capture()

    def p_capture(self):
        open_new("file:///home/lab246/Desktop/openpose_project_UI/photoCaptureCountdown.html")

        images_dir_path = "/home/lab246/Desktop/jpg_output"

        self.capture_images()
        image_files = [f for f in os.listdir(images_dir_path) if
                               os.path.isfile(os.path.join(images_dir_path, f))]
        highest = image_files[0]
        num = highest.split('_rendered.jpg')[0]
        for f in image_files:
            new_num = int(f.split('_rendered.jpg')[0])
            if new_num > num:
                num = new_num
                highest = f
        most_current = highest
        os.system("mv /home/lab246/Desktop/jpg_output/"+most_current + " /home/lab246/Desktop/webserver/saveTo/tosave.jpg")
        self.reset_folders()


    def p_save(self):
        open_new("file:///home/lab246/Desktop/openpose_project_UI/savePhoto.html")
        pass

    def gallery(self):
        open_new("file:///home/lab246/Desktop/openpose_project_UI/photoGalleryInformation.html")
        pass

s = State_Machine()