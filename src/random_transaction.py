import json
from typing import List
from google.cloud import bigquery
import sys
sys.path.append('shopping-cart-publisher/src/main.py')
from pub_sub import send_to_pubsub
import os

os.environ["GCLOUD_PROJECT"] = "valued-decker-380221"


def get_articles_data():
    query = """
        SELECT *
        FROM `valued-decker-380221.donnees_hm.articles`
    """
    all_articles = client.query(query).to_dataframe()
    return all_articles


# Initialize BigQuery client
client = bigquery.Client()


def get_random_user_id():
    # Fetch a random user from BigQuery
    query = """
        SELECT id
        FROM `valued-decker-380221.donnees_hm.clients`
        ORDER BY RAND()
        LIMIT 1
    """
    query_job = client.query(query)
    result = query_job.result()
    user_id = list(result)[0][0]
    return user_id


def create_message(user_id: str, article_id: List[int]) -> str:
    message = {
        "user_id": user_id,
        "articles_id": [int(article) for article in article_id]
    }
    return json.dumps(message)


# Load articles from CSV into a DataFrame
articles_df = get_articles_data()


def send_random_abandonned_cart():
    # Randomly assign 3 articles to the user
    random_articles = articles_df.sample(n=3)
    print("Randomly assigned articles:")
    print(random_articles['prod_name'])

    user_id = get_random_user_id()
    print("User ID:", user_id)

    article_ids = list(random_articles['article_id'].values)
    message = create_message(user_id, article_ids)
    send_to_pubsub(message)


send_random_abandonned_cart()

# while True:
#     send_random_abandonned_cart()
#     sleep(60)
