import sys, requests, jsonlines


def load_fixtures(filename):
    counter = 0
    for i in jsonlines.open(filename):
        counter+= 1
        print('posting item nr: ', counter)
        res = requests.post('http://localhost:1337/review/', json=i)
        print('response ', res)

if __name__ == "__main__":
    filename = str(sys.argv[1])
    if not filename:
        print('enter the name of the jsonfile')
    else:
        print(filename)
        load_fixtures(filename)
