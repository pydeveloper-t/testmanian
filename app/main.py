import argparse
from config import base_dir, log_dir,CONFIG
from testmanian import TestManian
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='https://www.tesmanian.com')
    parser.add_argument('--timeout', default=15, type=int)
    testmanian = TestManian(config=CONFIG)
    testmanian.run(timeout=parser.parse_args().timeout)


