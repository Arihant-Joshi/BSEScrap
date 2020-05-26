import time

t1 = time.time()
t2 = t1
while(t2-t1 < 10):
    t2 = time.time()
print(t2-t1)