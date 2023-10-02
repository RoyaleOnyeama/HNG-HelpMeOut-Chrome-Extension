# HNG-HelpMeOut Chrome Extension API Documentation
The **HNG-HelpMeOut Chrome Extension** is a screen recording chrome extension developed for HNGx Stage 5. This API, built with Flask, provides endpoints to manage screen recordings and retrieve video files.

## Base URL
The API is hosted at the following base URL:
Base URL: https://<hosted_url>/

## Endpoints

### 1. Create Video (POST)
    
- Create a new video record.
- Method: POST
- Endpoint: `https://<hosted_url>/api/recording`
- Response: JSON containing the created video ID.
    
    Example Request:

    ```bash
    curl -X POST https://<hosted_url>/api/recording
    ```
    
    Example Response:
    ```json
    {
        "recording_id": "1c1b55c6-31d7-4a3f-8f1e-4c344e51c1f0"
    }
    ```

### 2. Add Video Chunk to a Recording (POST)
    
- Add video chunks to an existing recording.
- Method: POST
- Endpoint: `https://<hosted_url>/api/recording/<vid_id>`
- Parameters:
  <vid_id> (string): The ID of the recording.
- Response: JSON indicating success.
    
    Example Request:
    ```bash
    curl -X POST https://<hosted_url>/api/recording/1c1b55c6-31d7-4a3f-8f1e-4c344e51c1f0 -d @video_chunk.mp4
    ```
    
    Example Response:
    ```json
    {
        "message": "Video chunk added successfully"
    }
    ```

### 3. Get Video of a Recording (GET)
    
- Retrieve the compiled video for a specific video ID.
- Method: GET
- Endpoint: /api/recording/<vid_id>
- Parameters:
  <vid_id> (string): The ID of the recording.
-Response: Video file.
    
    Example Request:
    ```bash
    curl https://<hosted_url>/api/recording/1c1b55c6-31d7-4a3f-8f1e-4c344e51c1f0
    ```

### 4. Get All Recordings of a User (GET)
    
- Retrieve all recordings associated with a specific user.
- Method: GET
- Endpoint: https://<hosted_url>/api/recording/user/<user_id>
- Parameters:
   <user_id> (string): The ID of the user.
-Response: JSON array of recording objects.
    
    Example Request:
    ```bash
    curl https://<hosted_url>/api/recording/user/user123
    ```

    Example Response:
    ```json
    [
        {
            "title": "recording1.mp4",
            "id": "1c1b55c6-31d7-4a3f-8f1e-4c344e51c1f0",
            "user_id": "user123",
            "time": "2023-10-02T12:34:56"
        },
        {
            "title": "recording2.mp4",
            "id": "2c2b55c6-31d7-4a3f-8f1e-4c344e51c1f1",
            "user_id": "user123",
            "time": "2023-10-02T13:45:00"
        }
    ]
    ```

### 5. Get All Recordings (GET)

- Retrieve all recordings.
- Method: GET
- Endpoint: https://<hosted_url>/api/recording
- Response: JSON array of recording objects.
    
    Example Request:
    ```bash
    curl https://<hosted_url>/api/recording
    ```

    Example Response:
    ```json
    [
        {
            "title": "recording1.mp4",
            "id": "1c1b55c6-31d7-4a3f-8f1e-4c344e51c1f0",
            "user_id": "",
            "time": "2023-10-02T12:34:56"
        },
        {
            "title": "recording2.mp4",
            "id": "2c2b55c6-31d7-4a3f-8f1e-4c344e51c1f1",
            "user_id": "",
            "time": "2023-10-02T13:45:00"
        }
    ]
    ```

### 6. Update Recording Title (PUT)
    
- Update the title of a recording.
- Method: PUT
- Endpoint: https://<hosted_url>/api/recording/<vid_id>
- Parameters:
    <vid_id> (string): The ID of the recording.
- Request Body: JSON with the new title.
    
    Example Request Body:
    ```json
    {
        "title": "new_title.mp4"
    }
    ```
    Response: JSON indicating success.

    Example Request:
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d '{"title":"new_title.mp4"}' https://<hosted_url>/api/recording/1c1b55c6-31d7-4a3f-8f1e-4c344e51c1f0
    ```

    Example Response:
    ```json
    {
        "message": "Recording title updated successfully"
    }
    ```

### 7. Delete a Recording (DELETE)
    
- Delete a recording.
- Method: DELETE
- Endpoint: https://<hosted_url>/api/recording/<vid_id>
- Parameters:
      <vid_id> (string): The ID of the recording.
- Response: JSON indicating success.
    
    Example Request:
    ```bash
    curl -X DELETE https://<hosted_url>/api/recording/1c1b55c6-31d7-4a3f-8f1e-4c344e51c1f0
    ```

    Example Response:
    ```json
    {
        "message": "Recording deleted successfully"
    }
    ```

## Usage

- Create a new video record using the POST /api/recording endpoint.

- Add video chunks to an existing recording using the POST /api/recording/<vid_id> endpoint.

- Retrieve the compiled video using the GET /api/recording/<vid_id> endpoint with the vid_id.

- Retrieve all recordings associated with a specific user using the GET /api/recording/user/<user_id> endpoint.

- Retrieve all recordings using the GET /api/recording endpoint.

- Update the title of a recording using the PUT /api/recording/<vid_id> endpoint.

- Delete a recording using the DELETE /api/recording/<vid_id> endpoint.

## Deployment
The API has been deployed and can be accessed at the provided base URL. Use the endpoints as described above to manage screen recordings.

## Known Limitations and Assumptions

