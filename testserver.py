import flask
import werkzeug.datastructures.file_storage

from Storage_Server.DataStorage import storage
import time

from Database_Management import user_relations

app = flask.Flask(__name__)
app.storage_bucket: storage.Database = storage.Database('database_config_bucket_one.json')
app.db: user_relations.Database = user_relations.Database(uri="bolt://192.168.0.207:7687",
                                                          auth=("neo4j", "adminadmin"))


@app.route('/upload_image_post', methods=['POST'])
def upload_image_post():
    if 'image' not in flask.request.files:
        return 'No image uploaded.', 400

    image_file: werkzeug.datastructures.file_storage.FileStorage = flask.request.files['image']

    bytes = image_file.read()
    print(type(bytes))

    hash_value = app.storage_bucket.calculate_hash(bytes)
    app.storage_bucket.upload_post(bytes, hash_value)

    app.db.create_image_post()

    return 'Image stored', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
