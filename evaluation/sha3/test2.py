from datetime import timedelta
from hashlib import sha3_256, sha3_384, sha3_512
import time
from timeit import default_timer as timer
import json
import pandas as pd

TEST_N = 1000

data = {
    "timestamp": time.time(),
    "pid": {},
}


def main():
    # a,b,c = 0,0,0

    i = 0
    while i <= TEST_N:

        # Method 1 : SHA3-256
        t = timer()
        sha3_256().update(json.dumps(data).encode())
        elaspsed_time = timer() - t

        eval_data = {'Method': 'SHA3-256', 'Length': f'{i}',
                     'Elasped Time (sec)': f'{timedelta(seconds=elaspsed_time)}'}
        s256 = elaspsed_time
        print(eval_data)


        # Method 2 : SHA3-384
        t = timer()
        sha3_384().update(json.dumps(data).encode())
        elaspsed_time = timer() - t

        eval_data = {'Method': 'SHA3-384', 'Length': f'{i}',
                     'Elasped Time (sec)': f'{timedelta(seconds=elaspsed_time)}'}
        s384 = elaspsed_time
        print(eval_data)


        # Method 3 : SHA3-512
        t = timer()
        sha3_512().update(json.dumps(data).encode())
        elaspsed_time = timer() - t

        eval_data = {'Method': 'SHA3-512', 'Length': f'{i}',
                     'Elasped Time (sec)': f'{timedelta(seconds=elaspsed_time)}'}
        s512 = elaspsed_time
        print(eval_data)

        
        # ====== Next Loop ======
        i += 1
        data['pid'][f'id{i}'] = "AAAA"

    #     if s256 > s384 and s256 > s512:
    #         a+=1
    #     elif s384 > s256 and s384 > s512:
    #         b+=1
    #     elif s512 > s256 and s512 > s384:
    #         c+=1
    #     else: pass

    # print(f"a:{a}, b:{b}, c:{c}")


if __name__ == '__main__':
    main()