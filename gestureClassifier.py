import json
from os import listdir
from os.path import isfile, join
from sklearn import tree
from sklearn.model_selection import cross_val_score


feature_names = ['right_arm_raised', 'left_arm_raised', 'knuckle_joints_up', 'knuckle_joints_down' ,'index_pointing_left' ,'index_pointing_right','thumb_tip_above_wrist','thumb_tip_below_wrist']
class_names = ['arms_raised', 'thumb_up', 'thumb_down', 'point_right', 'point_left']
def booleanToNum(bool):
    if bool:
        return 1
    else:
        return 0

# right arm raised
def right_arm_raised(keypoint_data):
    pose_data = keypoint_data['people'][0]['pose_keypoints_2d']
    return pose_data[7 * 3] < pose_data[6 * 3] < pose_data[5 * 3]


# left arm raised
def left_arm_raised(keypoint_data):
    pose_data = keypoint_data['people'][0]['pose_keypoints_2d']
    return pose_data[4 * 3] < pose_data[3 * 3] < pose_data[2 * 3]


# right arm lowered
def right_arm_lowered(keypoint_data):
    pose_data = keypoint_data['people'][0]['pose_keypoints_2d']
    return pose_data[7 * 3] > pose_data[6 * 3] > pose_data[5 * 3]


# left arm lowered
def left_arm_lowered(keypoint_data):
    pose_data = keypoint_data['people'][0]['pose_keypoints_2d']
    return pose_data[4 * 3] > pose_data[3 * 3] > pose_data[2 * 3]


# knuckle joints up
def knuckle_joints_up(keypoint_data):
    if left_arm_lowered(keypoint_data):
        # check right side
        right_hand = keypoint_data['people'][0]['hand_right_keypoints_2d']
        return right_hand[5 * 3] < right_hand[9 * 3] < right_hand[13 * 3] < right_hand[17 * 3]
    elif right_arm_lowered(keypoint_data):
        # check left side
        left_hand = keypoint_data['people'][0]['hand_left_keypoints_2d']
        return left_hand[5 * 3] <left_hand[9*3] < left_hand[13*3] < left_hand[17 * 3]
    else:
        return False


# knuckle joints down
def knuckle_joints_down(keypoint_data):
    if left_arm_lowered(keypoint_data):
        # check right side
        right_hand = keypoint_data['people'][0]['hand_right_keypoints_2d']
        return right_hand[5 * 3] > right_hand[9 * 3] > right_hand[13 * 3] > right_hand[17 * 3]
    elif right_arm_lowered(keypoint_data):
        # check left side
        left_hand = keypoint_data['people'][0]['hand_left_keypoints_2d']
        return left_hand[5 * 3] > left_hand[9*3] > left_hand[13*3] > left_hand[17 * 3]
    else:
        return False


# index pointing opposite of rest fingers (left)
def index_pointing_left(keypoint_data):
    if left_arm_lowered(keypoint_data):
        # check right side
        right_hand = keypoint_data['people'][0]['hand_right_keypoints_2d']
        index_finger = right_hand[8 * 3 + 1] < right_hand[7 * 3 + 1] < right_hand[6 * 3 + 1] < right_hand[5 * 3 + 1]
        middle_finger = right_hand[12 * 3 + 1] > right_hand[11 * 3 + 1] > right_hand[10 * 3 + 1]
        ring_finger = right_hand[16 * 3 + 1] > right_hand[15 * 3 + 1] > right_hand[14 * 3 + 1]
        pinky = right_hand[20 * 3 + 1] > right_hand[19 * 3 + 1] > right_hand[18 * 3 + 1]
        return index_finger and middle_finger and pinky and ring_finger
    elif right_arm_lowered(keypoint_data):
        # check left side
        left_hand = keypoint_data['people'][0]['hand_left_keypoints_2d']
        index_finger = left_hand[8 * 3 + 1] < left_hand[7 * 3 + 1] < left_hand[6 * 3 + 1] < left_hand[5 * 3 + 1]
        middle_finger = left_hand[12 * 3 + 1] > left_hand[11 * 3 + 1] > left_hand[10 * 3 + 1]
        ring_finger = left_hand[16 * 3 + 1] > left_hand[15 * 3 + 1] > left_hand[14 * 3 + 1]
        pinky = left_hand[20 * 3 + 1] > left_hand[19 * 3 + 1] > left_hand[18 * 3 + 1]
        return index_finger and middle_finger and pinky and ring_finger
    else:
        return False


# index pointing opposite of rest fingers (right)
def index_pointing_right(keypoint_data):
    if left_arm_lowered(keypoint_data):
        # check right side
        right_hand = keypoint_data['people'][0]['hand_right_keypoints_2d']
        index_finger = right_hand[8 * 3 + 1] > right_hand[7 * 3 + 1] > right_hand[6 * 3 + 1] > right_hand[5 * 3 + 1]
        middle_finger = right_hand[12 * 3 + 1] < right_hand[11 * 3 + 1] < right_hand[10 * 3 + 1]
        ring_finger = right_hand[16 * 3 + 1] < right_hand[15 * 3 + 1] < right_hand[14 * 3 + 1]
        pinky = right_hand[20 * 3 + 1] < right_hand[19 * 3 + 1] < right_hand[18 * 3 + 1]
        return index_finger and middle_finger and pinky and ring_finger
    elif right_arm_lowered(keypoint_data):
        # check left side
        left_hand = keypoint_data['people'][0]['hand_left_keypoints_2d']
        index_finger = left_hand[8 * 3 + 1] > left_hand[7 * 3 + 1] > left_hand[6 * 3 + 1] > left_hand[5 * 3 + 1]
        middle_finger = left_hand[12 * 3 + 1] < left_hand[11 * 3 + 1] < left_hand[10 * 3 + 1]
        ring_finger = left_hand[16 * 3 + 1] < left_hand[15 * 3 + 1] < left_hand[14 * 3 + 1]
        pinky = left_hand[20 * 3 + 1] < left_hand[19 * 3 + 1] < left_hand[18 * 3 + 1]
        return index_finger and middle_finger and pinky and ring_finger
    else:
        return False



# tip of thumb above wrist
def thumb_tip_above_wrist(keypoint_data):
    pose_data = keypoint_data['people'][0]['pose_keypoints_2d']
    if left_arm_lowered(keypoint_data):
        # check right side
        wrist = pose_data[3 * 7]
        right_hand = keypoint_data['people'][0]['hand_right_keypoints_2d']
        return right_hand[2 * 3] < wrist or right_hand[3 * 3] < wrist or right_hand[4 * 3] < wrist

    elif right_arm_lowered(keypoint_data):
        # check left side
        wrist = pose_data[3 * 4]
        left_hand = keypoint_data['people'][0]['hand_left_keypoints_2d']
        return left_hand[2*3] < wrist or left_hand[3*3] < wrist or left_hand[4*3] <wrist
    else:
        return False


# tip of thumb below wrist
def thumb_tip_below_wrist(keypoint_data):
    pose_data = keypoint_data['people'][0]['pose_keypoints_2d']
    if left_arm_lowered(keypoint_data):
        # check right side
        wrist = pose_data[3 * 7]
        right_hand = keypoint_data['people'][0]['hand_right_keypoints_2d']
        return right_hand[2 * 3] > wrist or right_hand[3 * 3] > wrist or right_hand[4 * 3] > wrist

    elif right_arm_lowered(keypoint_data):
        # check left side
        wrist = pose_data[3 * 4]
        left_hand = keypoint_data['people'][0]['hand_left_keypoints_2d']
        return left_hand[2 * 3] > wrist or left_hand[3 * 3] > wrist or left_hand[4 * 3] > wrist
    else:
        return False


def feature_generation(keypoint_data):
    features = []
    # right arm raised
    features.append(right_arm_raised(keypoint_data))

    # left arm raised
    features.append(left_arm_raised(keypoint_data))

    # knuckle joints up
    features.append(knuckle_joints_up(keypoint_data))

    # knuckle joints down
    features.append(knuckle_joints_down(keypoint_data))

    # index pointing opposite of rest fingers (left)
    features.append(index_pointing_left(keypoint_data))

    # index pointing opposite of rest fingers (right)
    features.append(index_pointing_right(keypoint_data))

    # tip of thumb above wrist
    features.append(thumb_tip_above_wrist(keypoint_data))

    # tip of thumb below wrist
    features.append(thumb_tip_below_wrist(keypoint_data))
    return [booleanToNum(x) for x in features]


# training

# take all the images and build a map
#   key is the name of the image
#   value is the features for that given image

keypoint_data_dir_path = '/Users/luisschubert/Desktop/openpose_trainingdata/keypoint_data/'
keypoint_data_files = [f for f in listdir(keypoint_data_dir_path) if isfile(join(keypoint_data_dir_path, f))]

training_data_map = {}

for keypoint_data_file in keypoint_data_files:
    keypoint_data = json.load(open(join(keypoint_data_dir_path,keypoint_data_file)))

    training_data_map[keypoint_data_file] = feature_generation(keypoint_data)

    # print(keypoint_data_file)
    # print(feature_names)
    # print(training_data_map[keypoint_data_file])
    # print("\n")


# convert training data map to features and classes

# classes :
    # 'arms_raised', 1
    # 'thumb_up_left', 'thumb_up_right', 2
    # 'thumb_down_left', 'thumb_down_right' 3
    # 'point-right_left', 'point-right_right' 4
    # 'point-left_left', 'point-left_right' 5

training_data_list =[]
training_label_list = []

for t_point_label in training_data_map:
    training_data_list.append(training_data_map[t_point_label])
    if 'both_hands_up' in t_point_label:
        training_label_list.append(1)
    elif 'thumb_up' in t_point_label:
        training_label_list.append(2)
    elif 'thumb_down' in t_point_label:
        training_label_list.append(3)
    elif 'point-right' in t_point_label:
        training_label_list.append(4)
    elif 'point-left' in t_point_label:
        training_label_list.append(5)
    else:
        print('UNRECOGNIZED TRAINING DATA')

clf = tree.DecisionTreeClassifier()

clf.fit(training_data_list, training_label_list)



# dotfile = open("dtree2.dot", 'w')
# dot_data = tree.export_graphviz(clf, out_file=dotfile,
#                          feature_names=feature_names,
#                          class_names=class_names,
#                          filled=True, rounded=True,
#                          special_characters=True)
# dotfile.close()

print(cross_val_score(clf, training_data_list, training_label_list, cv=10))



#
# graph = graphviz.Source( tree.export_graphviz(clf, out_file=None, feature_names=feature_names,
#                           class_names=class_names,
#                           filled=True, rounded=True,
#                           special_characters=True))
# graph.format = 'png'
# graph.render('dtree_render',view=True)


