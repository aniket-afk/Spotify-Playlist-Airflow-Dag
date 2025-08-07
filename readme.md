# Spotify API Airflow DAG

This repository contains an Apache Airflow Directed Acyclic Graph (DAG) for interacting with the Spotify API. The DAG performs two main tasks:
1. **Authorize User**: Obtains an access token from the Spotify API.
2. **Get Playlist**: Retrieves the user's playlists using the obtained access token.
![image](https://github.com/user-attachments/assets/77a82fd4-5c55-483d-9a34-8bf3d1ba226d)

## Setup

### Prerequisites

- Apache Airflow
- Python 3.x
- `requests` library
- `python-dotenv` library

### Installation

1. **Clone the Repository**:
```bash
   git clone <repository-url>
   cd <repository-directory>
```

2. **Create and Activate a Virtual Environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. **Install Dependencies**:
```bash
pip install requests python-dotenv apache-airflow
```

4. **Set Up Environment Variables:**
Create a .env file in the root directory with the following content:

```bash
TOKEN=<your-spotify-token>
CLIENT_ID=<your-spotify-client-id>
CLIENT_SECRET=<your-spotify-client-secret>
```

## DAG Configuration
1. DAG Name: spotify_dag
2. Schedule Interval: Daily (timedelta(days=1))
3. Start Date: August 6, 2024
4. Email Notifications: Disabled

### Tasks

1. ***authorize_user***:

 - Description: Authenticates with Spotify API and retrieves an access token.
 - Endpoint: POST https://accounts.spotify.com/api/token
 - Headers: Content-Type: application/x-www-form-urlencoded, Authorization: Basic <encoded-credentials>
 - Data: grant_type=client_credentials
 - XCom Key: spotify_token

2. ***get_playlist***:

 - Description: Fetches the user's playlists using the access token retrieved by authorize_user.
 - Endpoint: GET https://api.spotify.com/v1/me/playlists
 - Headers: Accept: application/json, Content-Type: application/json, Authorization: Bearer <token>
