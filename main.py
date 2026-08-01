from sys import argv

if __name__ == '__main__':
    if len(argv) == 2 and argv[1] == 'run':
        from app import create_app
        create_app().run()
    else:
        from reader import read_input
        read_input()