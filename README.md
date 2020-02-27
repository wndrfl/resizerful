# Resizerful

This is a serverless image handler wrapper

### Aws setup

To deploy this follow the following guide.

https://aws.amazon.com/solutions/serverless-image-handler/

This will set up a an api gateway endpoint, a lambda, and a
cloudfront distribution. At this point the image handler
will serve images.

To secure the images as suggested in the Security section of
the guide we are using signed URLs. Make sure you also secure
the following:

 - Make sure the S3 bucket is set to be private
 - Make sure the api gateway enpoint that calls the lambda
   is also private

Follow this section to secure the cloudfront distribution:

[Serving Private Content with Signed URLs and Signed Cookies](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/PrivateContent.html)

there are two main steps,

 - creating a [key value pair](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-trusted-signers.html#private-content-creating-cloudfront-key-pairs).
   Make sure you get the PEM file and make note of the key paid ID

 - restricting access under Cloudfront > Cloud Front distributions >
   the distribution > Behaviors tab > Edit > "Restrict Viewer Access" => Yes

### Install

```
pipenv install -e "git+https://github.com/wndrfl/resizerful.git#egg=resizerful"
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

In this case, the private key in the variable key is the contents of
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

### Troubleshooting

#### M2Crypto

M2Crypto likes python 2 better but it works fine with python 3. If pipenv
fails to build the M2Crypto wheel

```
sudo apt-get install libssl-dev swig
```

or in OSX

```
brew install openssl
brew install swig

env LDFLAGS="-L$(brew --prefix openssl)/lib" \
  CFLAGS="-I$(brew --prefix openssl)/include" \
  SWIG_FEATURES="-cpperraswarn -includeall -I$(brew --prefix openssl)/include" \
  pipenv install m2crypto
```

and then try installing this again.
