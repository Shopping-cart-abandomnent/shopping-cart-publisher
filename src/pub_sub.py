from google.cloud import pubsub_v1

project_id = "valued-decker-380221"
topic_id = "Shopping_Cart_Abandonment"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


def send_to_pubsub(message):
    data = message.encode("utf-8")
    future = publisher.publish(topic_path, data, origin="python-sample", username="gcp")
    msg_id = future.result()
    print(f"The message {msg_id} has been published to PubSub")
