import image_utils as utils
import face_detect as detect
import pic_edit as edit
import postprocess


def run_pipline(image_path, prompt):
    # retrieves and preprocesses the image
    converted = utils.preprocess(image_path)
    # saves the width and height of the original image for later uses
    width, height, exif = utils.get_shape(converted)
    print(width, height)
    print(exif)
    # box out the faces in the image
    rotation_flag = exif[274] if exif else 1
    masked = detect.detect_face(converted, rotation_flag)
    # replaces the faces with emojis
    results = edit.replace_with_emoji(masked, prompt)
    # post process the results
    return postprocess.postprocess(results, width, height)