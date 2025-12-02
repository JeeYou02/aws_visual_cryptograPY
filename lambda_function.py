import json
import base64
import cv2
import numpy as np

# --- Import all your utility functions ---
from vc_utils.rgb_to_greyscale import rgb_to_greyscale
from vc_utils.quantize_and_dither import quantize_and_dither
from vc_utils.key_gen_greyscale import key_gen_greyscale
from vc_utils.key_gen_binary import key_gen_binary
from vc_utils.encrypt_4levels import encrypt_4levels
from vc_utils.encrypt_binary import encrypt_binary
from vc_utils.VC_conversion import (
    VC_conversion_diagonal,
    VC_conversion_vertical,
    VC_conversion_horizontal,
    VC_conversion_greyscale_4levels
)
from vc_utils.superimpose import superimpose

N_LEVELS = 4

# --- Helper Functions for API data ---

def decode_image(img_b64, flags=cv2.IMREAD_COLOR):
    """Converts a base64 string to an OpenCV image."""
    img_bytes = base64.b64decode(img_b64)
    nparr = np.frombuffer(img_bytes, np.uint8)
    # flags=cv2.IMREAD_UNCHANGED is needed for alpha channels
    img = cv2.imdecode(nparr, flags)
    return img

def encode_image(img):
    """Converts an OpenCV image (with alpha) to a base64 string."""
    # Use .png to preserve transparency, which VC_conversion creates
    _, buffer = cv2.imencode('.png', img)
    img_b64 = base64.b64encode(buffer).decode('utf-8')
    return img_b64

def format_response(body_dict):
    """Creates a valid API Gateway 200 OK response."""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*', # Allow frontend to call
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body_dict)
    }

def format_error(message):
    """Creates a valid API Gateway 500 Error response."""
    return {
        'statusCode': 500,
        'headers': { 'Access-Control-Allow-Origin': '*' },
        'body': json.dumps({'error': message})
    }

# --- Action Handlers ---

def handle_encrypt(body):
    img = decode_image(body['image_b64'])

    # 1. Determine the key
    if body['key_option'] == 'generate':
        if body['conversion_type'] == 'binary':
            key_img = key_gen_binary(img)
        else: # greyscale
            key_img = key_gen_greyscale(img, N_LEVELS)
    else: # custom
        if 'custom_key_b64' not in body:
            raise ValueError("key_option was 'custom' but no custom_key_b64 provided.")
        key_img = decode_image(body['custom_key_b64'])

    # 2. Perform encryption
    if body['conversion_type'] == 'binary':
        # encrypt_binary does its own rgb_to_binary and negative
        cypher_img = encrypt_binary(img, key_img)
    else: # greyscale
        grey_img = rgb_to_greyscale(img)
        quantized_img = quantize_and_dither(grey_img.copy(), N_LEVELS)
        cypher_img = encrypt_4levels(quantized_img, key_img)

    # 3. Return both shares
    return format_response({
        'share1_b64': encode_image(key_img),
        'share2_b64': encode_image(cypher_img)
    })

def handle_transform(body):
    # For transformation, we need the alpha channel if it exists
    img = decode_image(body['image_b64'], cv2.IMREAD_UNCHANGED)
    
    if body['share_type'] == 'binary':
        transform_type = body.get('transform_type', 'vertical') # Default
        if transform_type == 'horizontal':
            vc_img = VC_conversion_horizontal(img)
        elif transform_type == 'diagonal':
            vc_img = VC_conversion_diagonal(img)
        else: # vertical
            vc_img = VC_conversion_vertical(img)
    else: # greyscale
        vc_img = VC_conversion_greyscale_4levels(img)

    return format_response({
        'transformed_image_b64': encode_image(vc_img)
    })

def handle_superimpose(body):
    # We MUST load with IMREAD_UNCHANGED to get the alpha channel
    img1 = decode_image(body['share1_b64'], cv2.IMREAD_UNCHANGED)
    img2 = decode_image(body['share2_b64'], cv2.IMREAD_UNCHANGED)

    output_img = superimpose(img1, img2)

    return format_response({
        'result_image_b64': encode_image(output_img)
    })

# --- Main Lambda Router ---

# --- Main Lambda Router ---

def lambda_handler(event, context):
    try:
        http_method = event['requestContext']['http']['method']
    except KeyError:
        http_method = event.get('httpMethod', 'POST')

    if http_method == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }

    elif http_method == 'POST':
        try:
            body = json.loads(event['body'])
            action = body.get('action')

            if action == 'encrypt':
                return handle_encrypt(body)
            elif action == 'transform':
                return handle_transform(body)
            elif action == 'superimpose':
                return handle_superimpose(body)
            else:
                return format_error(f"Invalid action: {action}")

        except Exception as e:
            return format_error(f"An exception occurred: {str(e)}")
            
    else:
        return format_error(f"Unsupported method: {http_method}")