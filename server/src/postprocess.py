import image_utils as utils

def postprocess(outputs, width, height):
    '''
    downloads the images from output and resizes them back to the original shape;
    returns a list of the saved image names
    
    output - a list of image urls
    width, height - the shape of the original image
    '''
    
    base_dir = 'tmp'
    res = []
    for i, url in enumerate(outputs):
        output_path = f'{base_dir}/out{i}.png'
        utils.retrieve_image(url, output_path)
        utils.resize_image(output_path, output_path, width, height)
        res.append(output_path)
    return res