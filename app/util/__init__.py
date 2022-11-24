import os
import copy
import errno
import hashlib

def mkdir_p(path):
    created_path = ''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    else:
        created_path = path
    finally:
        return created_path

def md5(fname):
    '''
    https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    '''
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def make_hash(o):
  """
  https://stackoverflow.com/questions/5884066/hashing-a-dictionary
  Makes a hash from a dictionary, list, tuple or set to any level, that contains
  only other hashable types (including any lists, tuples, sets, and
  dictionaries).
  """
  if isinstance(o, (set, tuple, list)):
    return tuple([make_hash(e) for e in o])
  elif not isinstance(o, dict):
    return hash(o)
  new_o = copy.deepcopy(o)
  for k, v in new_o.items():
    new_o[k] = make_hash(v)
  return hash(tuple(frozenset(sorted(new_o.items()))))

def build_url(*urlparts):
    return '/'.join([part.strip('/').lstrip('\\') for part in urlparts])
