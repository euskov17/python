import re
import zlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import os


class BlobType(Enum):
    """Helper class for holding blob type"""
    COMMIT = b'commit'
    TREE = b'tree'
    DATA = b'blob'

    @classmethod
    def from_bytes(cls, type_: bytes) -> 'BlobType':
        for member in cls:
            if member.value == type_:
                return member
        assert False, f'Unknown type {type_.decode("utf-8")}'


@dataclass
class Blob:
    """Any blob holder"""
    type_: BlobType
    content: bytes


@dataclass
class Commit:
    """Commit blob holder"""
    tree_hash: str
    parents: list[str]
    author: str
    committer: str
    message: str


@dataclass
class Tree:
    """Tree blob holder"""
    children: dict[str, Blob]


def read_blob(path: Path) -> Blob:
    """
    Read blob-file, decompress and parse header
    :param path: path to blob-file
    :return: blob-file type and content
    """
    with open(path, 'rb') as file:
        fl = file.read(-1)
        raw_blob = zlib.decompress(fl)
        head, content = raw_blob.split(b'\x00', maxsplit=1)
        type_ = BlobType(head.split()[0])
        blob = Blob(type_, content)

    return blob


def traverse_objects(obj_dir: Path) -> dict[str, Blob]:
    """
    Traverse directory with git objects and load them
    :param obj_dir: path to git "objects" directory
    :return: mapping from hash to blob with every blob found
    """
    blobs = dict()
    for folder in os.listdir(obj_dir):
        for obj in os.listdir(obj_dir / folder):
            hash_ = folder + obj
            blob = read_blob(obj_dir / folder / obj)
            blobs.update({hash_: blob})
    return blobs


def parse_commit(blob: Blob) -> Commit:
    """
    Parse commit blob
    :param blob: blob with commit type
    :return: parsed commit
    """
    header, body = [part.decode("utf-8") for part in blob.content.split(b"\n\n")]
    tree_hash = re.findall(r'tree\s[^\n]*\n', header)[0].rstrip('\n').split()[1]
    parents = [elem.split()[1] for elem in re.findall(r'parent\s[^\n]*\n', header)]
    author = " ".join(re.findall(r'author\s[^\n]*\n', header)[0].rstrip('\n').split()[1:])
    committer = " ".join(re.findall(r'committer\s[^\n]*', header)[0].rstrip('\n').split()[1:])
    message = body.rstrip('\n')
    return Commit(tree_hash, parents, author, committer, message)


def parse_tree(blobs: dict[str, Blob], tree_root: Blob, ignore_missing: bool = True) -> Tree:
    """
    Parse tree blob
    :param blobs: all read blobs (by traverse_objects)
    :param tree_root: tree blob to parse
    :param ignore_missing: ignore blobs which were not found in objects directory
    :return: tree contains children blobs (or only part of them found in objects directory)
    NB. Children blobs are not being parsed according to type.
        Also nested tree blobs are not being traversed.
    """
    children = {}
    for elem in tree_root.content.split(b' ')[1:]:
        hash_ = elem.split(b'\0', maxsplit=1)[1][:20].hex()
        name = elem.split(b'\0', maxsplit=1)[0].decode('utf-8')
        if hash_ in blobs.keys():
            children.update({name: blobs[hash_]})
    return Tree(children)


def find_initial_commit(blobs: dict[str, Blob]) -> Commit:
    """
    Iterate over blobs and find initial commit (without parents)
    :param blobs: blobs read from objects dir
    :return: initial commit
    """
    for name, blob in blobs.items():
        if blob.type_ == BlobType(b'commit'):
            elem = parse_commit(blob)
            if len(elem.parents) == 0:
                return elem
    return Commit("", [""], "", "", "")


def search_file(blobs: dict[str, Blob], tree_root: Blob, filename: str) -> Blob:
    """
    Traverse tree blob (can have nested tree blobs) and find requested file,
    check if file was not found (assertion).
    :param blobs: blobs read from objects dir
    :param tree_root: root blob for traversal
    :param filename: requested file
    :return: requested file blob
    """
    tree = parse_tree(blobs, tree_root)
    for name, blob in tree.children.items():
        if name == filename:
            return blob
        else:
            if blob.type_ == BlobType(b'tree'):
                attempt = search_file(blobs, blob, filename)
                if attempt != blob:
                    return attempt
            else:
                continue
    return tree_root
