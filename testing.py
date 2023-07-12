import hashlib
from Storage_Server.DataStorage import storage
from PIL import Image
from io import BytesIO
import os
import warnings


def calculate_hash(data: bytes, chunk_size: int = 4096):
    _hash = hashlib.sha256()
    while True:
        byte_block = data[:chunk_size]
        if not byte_block:
            break
        _hash.update(byte_block)
        data = data[chunk_size:]
    return _hash.hexdigest()


def remove_metadata(image_bytes) -> bytes | None:
    try:
        image = Image.open(BytesIO(image_bytes))

        image = image.convert("RGB")
        image_info = image.info.copy()
        for key in image_info:
            if key in ("exif", "icc_profile"):
                del image.info[key]

        output_buffer = BytesIO()
        image.save(output_buffer, format="JPEG", optimize=True)

        modified_bytes = output_buffer.getvalue()

        size_difference = len(image_bytes) - len(modified_bytes)
        if size_difference < 0:
            warnings.warn(
                "File got larger through removal of metadata.\n"
                f"\tBefore: {calculate_hash(image_bytes)} \t| {len(image_bytes)} "
                f"bytes\n\t"
                f"After: {calculate_hash(modified_bytes)} \t| {len(modified_bytes)} "
                f"bytes\n\tSize difference: {size_difference} bytes"
            )

        print("Metadata removed successfully.")
        print("Size difference: {} bytes".format(size_difference))

        return modified_bytes
    except Exception as e:
        print("An error occurred while removing metadata:", str(e))
        return None


def main():
    db = storage.Database(
        db_config=r"C:\Users\Flinn\Documents\Social-Clone"
        r"\database_config_bucket_one.json"
    )
    db.init_database()

    while True:
        filepath = input("Filepath: ")
        if filepath:
            with open(filepath, "rb") as f:
                sha256_hash = hashlib.sha256()
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
                print(sha256_hash.hexdigest())
                f.seek(0)
                print(calculate_hash(f.read()))

                f.seek(0)
                y = db.upload_post(post=f.read(), hash_val=sha256_hash.hexdigest())
                print(y)
        else:
            hash_to_del = input("Enter hash value to delete: ")
            exists_to_del = db.check_for_existence(hash_to_del)
            print("Exists: ", exists_to_del)
            if exists_to_del:
                db.delete_post(hash_to_del)

                exists_to_del = db.check_for_existence(hash_to_del)
                print("Exists: ", exists_to_del)


if __name__ == "__main__":
    # Example usage
    main()
    r"""
    image_path = r"C:\Users\Flinn\Downloads\941-1080x900.jpg"
    output_path = r"C:\Users\Flinn\Downloads\941-1080x900_2.jpg"
    with open(image_path, 'rb') as file:
        x = remove_metadata(file.read())
        with open(output_path, 'wb') as save_file:
            save_file.write(x)
    """
