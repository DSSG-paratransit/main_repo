if __name__ == "__main__":
    import os
    import time

    for i in range(10):
        time.sleep(1)
        print(i)
    f  = open(os.path.join('data','flag.txt'),'w')
    f.write(400)
    
        
    
    #raise ValueError('Error!')       