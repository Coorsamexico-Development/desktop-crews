
from google.cloud import storage

def authenticate_implicit_with_adc(project_id="your-google-cloud-project-id"):
    storage_client = storage.Client.from_service_account_json(credentials="cr")
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")


