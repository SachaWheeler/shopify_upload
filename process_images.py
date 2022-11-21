import datetime
import os
import glob
import cv2
import base64
import json
# import shopify
from utils import SHOPIFY_ACCESS_TOKEN, SHOPIFY_API_KEY, SHOPIFY_API_SECRET


shop_url = "https://%s:%s@drawing-machine.myshopify.com/admin" % (SHOPIFY_API_KEY, SHOPIFY_API_SECRET)

today = str(datetime.date.today())
input_dir = 'input/'
output_dir = f'output/{today}/'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# read input dir
image_list = glob.glob(f"{input_dir}/*.JPG")
sorted_images = sorted(image_list)
MARGIN_LEFT   = 100
MARGIN_RIGHT  = 500
MARGIN_TOP    = 100
MARGIN_BOTTOM = 300
for file in sorted_images:
    print(file)
    _, filename = file.split('/')
    print(filename)
    img = cv2.imread(file)
    height, width, channels = img.shape
    print(height, width, channels)
    y = MARGIN_TOP
    x = MARGIN_LEFT
    h = height - MARGIN_BOTTOM
    w = width - MARGIN_RIGHT
    #   crop
    crop_img = img[y:y+h, x:x+w]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)

    #   rotate
    rot_img = cv2.rotate(crop_img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow("rotated", rot_img)
    cv2.waitKey(0)

    #   straighten ?
    #   save to output dir
    cv2.imwrite(f"{output_dir}{filename}", rot_img)
    #   remove from input dir
    retval, buffer = cv2.imencode('.jpg', rot_img)
    jpg_as_text = base64.b64encode(buffer)
    print(jpg_as_text)

    # Create a new product
    """
    {"product": {
        "title": "Burton Custom Freestyle 151",
        "body_html": "<strong>Good snowboard!</strong>",
        "vendor": "Burton",
        "product_type": "Snowboard",
        "tags": [
            "Barnes & Noble",
            "Big Air",
            "John's Fav"
        ]
    } }

    curl -d '{"product":{"title":"Burton Custom Freestyle 151","body_html":"<strong>Good snowboard!</strong>","vendor":"Burton","product_type":"Snowboard","tags":["Barnes & Noble","Big Air","John's Fav"]}}' \
-X POST "https://your-development-store.myshopify.com/admin/api/2022-10/products.json" \
-H "X-Shopify-Access-Token: {access_token}" \
-H "Content-Type: application/json"

    """

    # Attach a primary image to it
    """
    "image": {
        "position":1,
        "attachment": "R0lGODlhbgCEdZ97\n4qNe+bonfvCfVXvly1762beOOdLBd+Q7PCAAOw==\n",
        "filename": "rails_logo.gif"
    }
}
    -X POST "https://your-development-store.myshopify.com/admin/api/2022-10/products/632910392/images.json" \
-H "X-Shopify-Access-Token: {access_token}" \
-H "Content-Type: application/json"
    """


# for each in output dir
#   post new product to shopify

