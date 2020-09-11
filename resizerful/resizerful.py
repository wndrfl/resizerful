import json
import base64
import rsa
import time


class Resizerful:
    DEFAULT_SETTINGS = {
        'bucket_name': None,
        'key_pair_id': None,
        'private_key': None,
        'cf_base_url': None,
        'aws_encode_translation': bytes.maketrans(b'+=/', b'-_~'),
        'default_width': 320,
        'default_fit': 'cover',
        'url_duration': 60 * 30  # 30 minutes (Unit is seconds)
    }

    def __init__(self, **kwargs):
        for setting in self.DEFAULT_SETTINGS:
            if setting in kwargs:
                setattr(self, setting, kwargs[setting])
            else:
                setattr(self, setting, self.DEFAULT_SETTINGS[setting])

    def aws_safe_b64encode(self, s):
        return base64.b64encode(s).translate(bytes.maketrans(b'+=/', b'-_~'))

    def sign_string(self, message, priv_key_string):
        # Make sure message and private key are in bytes format so we can support more inputs
        if not hasattr(message, 'decode'):
            message = message.encode('utf-8')

        if not hasattr(priv_key_string, 'decode'):
            priv_key_string = priv_key_string.encode('utf-8')

        key = rsa.PrivateKey.load_pkcs1(priv_key_string)
        signature = rsa.sign(message, key, 'SHA-1')
        return self.aws_safe_b64encode(signature).decode('utf-8')

    def resize_image_url(self, image_name, grayscale=False, flatten=False, flip=False, flop=False, negate=False,
                         normalise=False, **kwargs):
        """
        resizes an image, there are many options available, like,

        {
          "bucket": "wonderful-memes",
          "key": "IMG_20190315_191901.jpg",
          "edits": {
            "resize": {
              "fit": "cover",
              "background": {
                "r": 255,
                "g": 0,
                "b": 255,
                "alpha": 1
              }
            },
            "flatten": true,
            "grayscale": true,
            "flip": true,
            "flop": true,
            "negate": true,
            "normalise": true,
            "tint": {
              "r": 255,
              "g": 0,
              "b": 255
            },
            "smartCrop": {
              "faceIndex": 2,
              "padding": 5
            }
          }
        }
        We are assuming we are always resizing and then adding a few optional edits
        """

        image_options = {
            "bucket": self.bucket_name,
            "key": image_name,
            "edits": {
                "resize": {
                    "width": self.default_width,
                    "fit": self.default_fit,
                },
            }
        }
        if 'width' in kwargs:
            image_options['edits']['resize']['width'] = kwargs['width']
        if 'height' in kwargs:
            image_options['edits']['resize']['height'] = kwargs['height']
        if 'fit' in kwargs:
            image_options['edits']['resize']['fit'] = kwargs['fit']
        if grayscale:
            image_options['edits']['grayscale'] = True
        if flatten:
            image_options['edits']['flatten'] = True
        if flip:
            image_options['edits']['flip'] = True
        if flop:
            image_options['edits']['flop'] = True
        if negate:
            image_options['edits']['negate'] = True
        if normalise:
            image_options['edits']['normalize'] = True

        options_string = json.dumps(image_options, indent=None, separators=(',', ':'))

        # The aws Serverless Image re-sizer likes base64 encoding. doing the aws
        # specific encoding like so was breaking the app:
        #   uri = self.aws_safe_b64encode(options_string.encode('utf-8')).decode('utf-8')
        # If the image re-sizer doesn't like urlsafe_b64encode at some point we
        # can also try:
        # uri = base64.b64encode(options_string.encode('utf-8')).decode('utf-8')
        uri = base64.urlsafe_b64encode(options_string.encode('utf-8')).decode('utf-8')

        return f'{self.cf_base_url}{uri}'

    def sign_url(self, url):
        policy = {
            "Statement": [
                {
                    "Resource": url,
                    "Condition": {
                        "DateLessThan": {
                            "AWS:EpochTime": int(time.time()) + self.url_duration
                        }
                    }
                }
            ]
        }
        json_policy = json.dumps(policy, indent=None, separators=(',', ':'))
        encoded_policy = self.aws_safe_b64encode(json_policy.encode('utf-8')).decode('utf-8')
        signature = self.sign_string(json_policy, self.private_key)
        return f'{url}?Policy={encoded_policy}&Signature={signature}&Key-Pair-Id={self.key_pair_id}'

    def signed_resize_url(self, image_name, **kwargs):
        image_url = self.resize_image_url(image_name, **kwargs)
        return self.sign_url(image_url)

    def unsigned_resize_url(self, image_name, **kwargs):
        image_url = self.resize_image_url(image_name, **kwargs)
        return image_url
