import multiprocessing as mp
import time

def test(val):
    print(val.value)
    time.sleep(3)
    print(val.value)

def main():
    val = mp.Value('i', 0)
    p = mp.Process(target=test, args=(val,))
    p.start()
    time.sleep(1)
    val.value = 5


if __name__ == '__main__':
    main()
