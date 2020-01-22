# Resizeful

This is a serverless image handler wrapper

https://aws.amazon.com/solutions/serverless-image-handler/

### Aws setup

To deploy this basically follow the tutorial on the previous link.
Also in the console logging in as the root account create a key value 
pair for cloud front as described here

https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-trusted-signers.html#private-content-creating-cloudfront-key-pairs

Make sure you get the PEM file and make not of the key paid ID

### Install

Set up a github personal access token for this
https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

```
pipenv install --verbose -e "git+https://manuelisimo:yourpersonaltoken@github.com/wndrfl/resizerful.git#egg=resizerful"
```

### Usage

Upload images to an S3 bucket using your favorite method. e.g.

```
client = boto3.client('s3', region_name='us-west-2')
client.upload_file('escape.jpg', 'wonderful-memes', 'escape.jpg')
```

Then keep track of the bucket name and image name in the bucket.
Now you can create a Resizerful object and call signed_resize_url
in this fashion

```
key = '''  ...  '''
resizer = Resizerful(
    bucket_name='wonderful-memes',
    cf_base_url='https://dzzplw659h3bu.cloudfront.net/',
    key_pair_id='APKAJXOKVLCWKI726JTA',
    private_key=key
)
signed_url = resizer.signed_resize_url('escape.jpg')
print(signed_url)
```

in this case, the private key in the variable key is the contents of
the PEM file from the cloudfront distribution.

Resizerful takes 4 required parameters

| argument | Notes |
|----------|-------|
| bucket_name | S3 bucket |
| cf_base_url | base path of the clouldfront distribution |
| key_pair_id | key pair id of the cloudfront distribution |
| private_key | contents of PEM file of the key pair being used |

signed_resize_url takes many parameters, including:

| width | width |
|-------|-------|
| height | height |
| fit | One of ('cover', 'contain', 'fill', 'inside', 'outside') |
| grayscale | grayscale filter |
| flatten | flattens the image, whatever that means |
| flip | flips image vertically |
| flop | flops image horizontally |
| negate | some sort of retro filter |
| normalise | another filter |
