import random
def random_ip(rows):
    ip_lists=[]
    for row in rows:

        ip_lists.append({"http":str(row[0])+":"+str(row[1])})
    return ip_lists

def random_apple():
    return random.randint(200,537)

def random_chrome():
    return random.randint(500,3300)
