def testapp():
    while True:
        echo = str(input('user input: '))
        if echo == "break":
            break
        print(f'Echo: {echo}')

testapp()