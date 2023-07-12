import hashlib


def calculate_hash(data: bytes, chunk_size: int = 4096):
    _hash = hashlib.sha256()
    while True:
        byte_block = data[:chunk_size]
        if not byte_block:
            break
        _hash.update(byte_block)
        data = data[chunk_size:]
    return _hash.hexdigest()


def main():
    db = storage.Database()
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

                x = db.check_for_existence(sha256_hash.hexdigest())
                print(x)
                if not x:
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
    main()
