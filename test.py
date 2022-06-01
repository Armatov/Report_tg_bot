from time import gmtime, sleep, localtime, strftime


while True:
    
    
    time_mday = localtime().tm_mday
    time_hour = gmtime().tm_hour
    time_min  = gmtime().tm_min
    time_sec = localtime().tm_sec
    time_mon = localtime().tm_mon
    print(strftime(f"сейчас вренмени: %H:%M:%S. день %A"))
    sleep(1)

