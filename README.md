# HNG-HelpMeOut-Chrome-Extension

The **HelpMeOut Chrome Extension** is a screen recording chrome extension created for HNGx Stage 5. The Python framework, Flask was used for the backend.

## Endpoints

### Create Video (POST)

- Create a new video record.
- Method: POST
- Endpoint: `https://<hosted_url>/create/`
- Response: JSON containing the created video ID.

Example Request:
```bash
curl -X POST https://<hosted_url>/create/
```

Example Response:
```json
{
    "video_id": 1
}
```

### Get Video (GET)

- Retrieve the compiled video for a specific video ID.
- Method: GET
- Endpoint: `https://<hosted_url>/get/<video_id>/`
- Response: Video file.

Example Request:
```bash
curl https://<hosted_url>/get/1/
```

## Usage

1. Create a new video record using the "Create" endpoint.

2. Retrieve the compiled video using the "Get" endpoint with the `video_id`.

## Deployment

The API has been deployed and can be accessed at the following base URL:
- Base URL: `https://<hosted_url>/`

## Known Limitations and Assumptions
