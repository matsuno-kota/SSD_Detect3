from keras import backend as K
from keras.preprocessing import image
from imageio import imread
import numpy as np
from matplotlib import pyplot as plt
from ssd_encoder_decoder.ssd_output_decoder import decode_detections, decode_detections_fast
import cv2

def ssd_detect(ori_img, model):

    # Set the image size.
    img_height = 512
    img_width = 512

    # ## 2. Load some images
    #
    # Load some images for which you'd like the model to make predictions.

    # In[4]:


    orig_images = [] # Store the images here.
    input_images = [] # Store resized versions of the images here.
    object_points = [] # Store detected object points

    # We'll only load one image in this example.

    orig_images.append(ori_img)
    img = cv2.resize(ori_img,(img_width,img_height))
    img = image.img_to_array(img)
    input_images.append(img)
    input_images = np.array(input_images)


    # ## 3. Make predictions

    # In[6]:


    y_pred = model.predict(input_images)

    # `y_pred` contains a fixed number of predictions per batch item (200 if you use the original model configuration), many of which are low-confidence predictions or dummy entries. We therefore need to apply a confidence threshold to filter out the bad predictions. Set this confidence threshold value how you see fit.

    # In[7]:
    # 4: Decode the raw predictions in `y_pred`.

    y_pred_decoded = decode_detections(y_pred,
                                       confidence_thresh=0.3,
                                       iou_threshold=0.4,
                                       top_k=200,
                                       normalize_coords=True,
                                       img_height=img_height,
                                       img_width=img_width)

    # 5: Convert the predictions for the original image.

    np.set_printoptions(precision=2, suppress=True, linewidth=90)
    print("Predicted boxes:\n")
    print('   class   conf xmin   ymin   xmax   ymax')
    print(y_pred_decoded[0])# ## 4. Visualize the predictions
    #
    # We just resized the input image above and made predictions on the distorted image. We'd like to visualize the predictions on the image in its original size though, so below we'll transform the coordinates of the predicted boxes accordingly.

    # In[7]:


    # Display the image and draw the predicted boxes onto it.

    # Set the colors for the bounding boxes
    colors = plt.cm.hsv(np.linspace(0, 1, 3)).tolist()
    classes = ['background',
               'bottle', 'lego']

    plt.figure(figsize=(8,6))
    plt.imshow(orig_images[0])

    current_axis = plt.gca()

    for box in y_pred_decoded[0]:
        # Transform the predicted bounding boxes for the 512x512 image to the original image dimensions.
        xmin = box[-4] * orig_images[0].shape[1] / img_width
        ymin = box[-3] * orig_images[0].shape[0] / img_height
        xmax = box[-2] * orig_images[0].shape[1] / img_width
        ymax = box[-1] * orig_images[0].shape[0] / img_height
        color = colors[int(box[0])]
        label = '{}: {:.2f}'.format(classes[int(box[0])], box[1])
        current_axis.add_patch(plt.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, color=color, fill=False, linewidth=2))
        current_axis.text(xmin, ymin-30, label, size='x-large', color='white', bbox={'facecolor':color, 'alpha':1.0})
        object_points.append([box[0], (xmax+xmin)/2, (ymax+ymin)/2])
    #plt.show()
    return object_points
