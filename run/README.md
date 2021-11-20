## Setup

**Set project**

```
PROJECT=<your project>
```

**Set defaults**

```
gcloud config set run/platform managed
gcloud config set run/region europe-west1
gcloud config set eventarc/location europe-west1
```

https://cloud.google.com/eventarc/docs/run/quickstart-storage#before-you-begin
```
SERVICE_ACCOUNT="$(gsutil kms serviceaccount -p $PROJECT)"

gcloud projects add-iam-policy-binding $PROJECT \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role='roles/pubsub.publisher'
```

### Build & Deploy

```
TAG=gcr.io/$PROJECT/$(basename "$PWD")py
gcloud builds submit --tag $TAG
gcloud run deploy $NAME --image $TAG
```

#### Set environment variable

```bash
gcloud run services update --platform=managed --region=europe-west1 --update-env-vars NAME=Magnus
```

### Create Cloud Run trigger

```
gcloud eventarc triggers create imageprocessing-image-uploaded-v5  \
--location=europe-west1 \
--destination-run-service=imageprocessingpy \
--destination-run-path="/" \
--destination-run-region=europe-west1 \
--event-filters="type=google.cloud.storage.object.v1.finalized" \
--event-filters="bucket=imageprocessing-upload" \
--service-account=trigger-cloud-storage@training-ground-330518.iam.gserviceaccount.com
```



### Potential TODO
* Add possibility to upload file from website
* Find a nicer way of refreshing the static page
* Turn Cloud Run functions into Cloud Functions
* Use terraform to deploy
