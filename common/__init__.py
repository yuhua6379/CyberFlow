import hashlib


def md5(key_str: str):
    digest = hashlib.md5(key_str.encode('utf-8')).digest()

    # 将哈希值转换为十六进制字符串
    md5s = int.from_bytes(digest, byteorder="big").to_bytes(length=16, byteorder="big").hex()
    return md5s
