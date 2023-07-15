import uuid

import flask
import werkzeug.datastructures.file_storage

from Storage_Server.DataStorage import storage
import time

from Database_Management import user_relations

app = flask.Flask(__name__)
app.storage_bucket: storage.Database = storage.Database(
    "database_config_bucket_one.json"
)
app.db: user_relations.Database = user_relations.Database(
    uri="bolt://192.168.0.207:7687", auth=("neo4j", "adminadmin")
)

"""
app.db.add_user(
    user_relations.User(
        username="flinn",
        email="flinn.realmail@test.com",
        password="fakmwdkja",
        date_of_birth=time.time() - 10000,
        date_of_joining=time.time(),
    )
)
"""


@app.route("/upload_image_post", methods=["POST"])
def upload_image_post():
    if "image" not in flask.request.files:
        return "No image uploaded.", 400

    image_file: werkzeug.datastructures.file_storage.FileStorage = flask.request.files[
        "image"
    ]

    bytes = image_file.read()
    print(type(bytes))

    hash_value = app.storage_bucket.calculate_hash(bytes)

    post = user_relations.ImagePost(
        id=uuid.uuid4(),
        hash=hash_value,  # noqa
        description="Some post I took on the north sea",
        creator="flinn",
        upload_time=time.time(),
        tags=[],
    )

    app.storage_bucket.upload_post(bytes, hash_value)
    app.db.create_image_post(post)

    return "Image stored", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
