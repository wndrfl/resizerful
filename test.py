# boto3 is not a dependency for Resizerful but for testing it is often
# useful so we can upload things

# import boto3
from resizerful import Resizerful

if __name__ == '__main__':
    # Upload file, maybe
    # client = boto3.client('s3', region_name='us-west-2')
    # client.upload_file('escape.jpg', 'wonderful-memes', 'escape.jpg')

    key = '''  ...private key goes here...  '''

    resizer = Resizerful(
        bucket_name='wonderful-memes',
        cf_base_url='https://dzzplw659h3bu.cloudfront.net/',
        key_pair_id='APKAJXOKVLCWKI726JTA',
        private_key=key
    )
    signed_url = resizer.signed_resize_url('escape.jpg', width=256, height=256)
    print(signed_url)
