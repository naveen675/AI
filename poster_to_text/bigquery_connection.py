
from google.cloud import bigquery
from google.cloud import bigquery_connection_v1 as bq_connection
from config import PROJECT_ID,CONN_NAME,DATASET_ID,OBJECT_TABLE_NAME,REGION,CONN_NAME,VISION_MODEL_NAME,TRANSLATE_MODEL_NAME,NLP_MODEL_NAME,BUCKET_LOC


#serviceAccount:bqcx-475064263073-kxi2@gcp-sa-bigquery-condel.iam.gserviceaccount.com
#gcloud projects add-iam-policy-binding 'genia-data-pipe' --condition=None --no-user-output-enabled --member='serviceAccount:bqcx-475064263073-kxi2@gcp-sa-bigquery-condel.iam.gserviceaccount.com' --role='roles/cloudtranslate.user'
#gcloud projects add-iam-policy-binding 'genia-data-pipe' --condition=None --no-user-output-enabled --member='serviceAccount:bqcx-475064263073-kxi2@gcp-sa-bigquery-condel.iam.gserviceaccount.com' --role='roles/serviceusage.serviceUsageConsumer'

client = bq_connection.ConnectionServiceClient()
new_conn_parent = f"projects/{PROJECT_ID}/locations/US"
exists_conn_parent = f"projects/{PROJECT_ID}/locations/US/connections/{CONN_NAME}"
cloud_resource_properties = bq_connection.CloudResourceProperties({})

# try:
#     request = client.get_connection(
#         request=bq_connection.GetConnectionRequest(name=exists_conn_parent)
#     )
#     CONN_SERVICE_ACCOUNT = f"serviceAccount:{request.cloud_resource.service_account_id}"
# except Exception:
#     connection = bq_connection.types.Connection(
#         {"friendly_name": CONN_NAME, "cloud_resource": cloud_resource_properties}
#     )
#     request = bq_connection.CreateConnectionRequest(
#         {
#             "parent": new_conn_parent,
#             "connection_id": CONN_NAME,
#             "connection": connection,
#         }
#     )
#     response = client.create_connection(request)
#     CONN_SERVICE_ACCOUNT = (
#         f"serviceAccount:{response.cloud_resource.service_account_id}"
#     )
# print(CONN_SERVICE_ACCOUNT)


client = bigquery.Client(project=PROJECT_ID)
# dataset = client.create_dataset(DATASET_ID, exists_ok=True)
# print(f"Dataset {dataset.dataset_id} created.")

def run_bq_query(sql: str):
    """
    Input: SQL query, as a string, to execute in BigQuery
    Returns the query results or error, if any
    """
    try:
        query_job = client.query(sql)
        result = query_job.result()
        print(f"JOB ID: {query_job.job_id} STATUS: {query_job.state}")
        return result

    except Exception as e:
        raise Exception(str(e))

# sql = f"""
#       CREATE OR REPLACE EXTERNAL TABLE
#         `{PROJECT_ID}.{DATASET_ID}.{OBJECT_TABLE_NAME}`
#       WITH
#         CONNECTION `{REGION}.{CONN_NAME}`
#         OPTIONS
#           (object_metadata = 'SIMPLE', uris = ['{BUCKET_LOC}/*']);
#       """
# result = run_bq_query(sql)
# print(result)



# sql = f"""
#         SELECT
#             *
#         FROM
#             `{PROJECT_ID}.{DATASET_ID}.{OBJECT_TABLE_NAME}`
#         LIMIT
#             50;
#       """
# result = run_bq_query(sql)
# result.to_dataframe().head(10)
# print(result[0])


# sql = f"""
#       CREATE OR REPLACE MODEL
#         `{PROJECT_ID}.{DATASET_ID}.{VISION_MODEL_NAME}`
#       REMOTE WITH
#           CONNECTION `{PROJECT_ID}.{REGION}.{CONN_NAME}`
#           OPTIONS ( remote_service_type = 'cloud_ai_vision_v1' );
#         """
# result = run_bq_query(sql)


# sql = f"""
#         CREATE OR REPLACE TABLE
#           `{PROJECT_ID}.{DATASET_ID}.translated_results` AS
#         SELECT
#           STRING(ml_translate_result.translations[0].detected_language_code)
#            as original_language,
#           STRING(ml_translate_result.translations[0].translated_text)
#            as translated_title,
#           *
#         FROM
#           ML.TRANSLATE(
#             MODEL `{PROJECT_ID}.{DATASET_ID}.{TRANSLATE_MODEL_NAME}`,
#             TABLE `{DATASET_ID}.image_results`,
#             STRUCT(
#             'TRANSLATE_TEXT' as translate_mode,
#             "en" as target_language_code
#             )
#           );
#         """

sql = f"""
      CREATE OR REPLACE TABLE
        `{PROJECT_ID}.{DATASET_ID}.image_results` AS
      SELECT
        
        REPLACE(
          STRING(
            ml_annotate_image_result.full_text_annotation.text),
            '\n', ' '
        ) AS text_content,
        *
      FROM
        ML.ANNOTATE_IMAGE(
          MODEL `{PROJECT_ID}.{DATASET_ID}.{VISION_MODEL_NAME}`,
          TABLE `{DATASET_ID}.{OBJECT_TABLE_NAME}`,
          STRUCT(['TEXT_DETECTION'] AS vision_features));
      """
run_bq_query(sql)



