import getopt
import os
import sys

from fabric import Connection


def deploy(c, file, namespace, timeout):
    c.put(f'{file}',
          f'/tmp/deploy.yml')
    c.run(f'kubectl config set-context --current --namespace={namespace}')
    c.run('kubectl apply -f /tmp/deploy.yml')
    c.run(f'kubectl rollout status deployment -f /tmp/deploy --timeout={timeout}m')
    c.run('rm /tmp/deploy.yml')


def usage():
    print("Usage: " + sys.argv[0] + " [OPTIONS]")
    print("\t-p\t\tPort Number, defaults to 22")
    print("\t-u\t\tUsername, defaults to deploy")
    print("\t-k\t\tSSH Key File, defaults to ~/.ssh/id_rsa")
    print("\t-h\t\tHost, defaults to 127.0.0.1")
    print("\t-v\t\tVerbose, defaults to False")
    print("\t--help          \tThis help menu\n")
    print("Example:")
    print("\t" + sys.argv[0] +
          " -h localhost -p 22 -k ~/.ssh/id_rsa -u my_user")


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:u:k:n:f:t:", ["help"])
    except getopt.GetoptError as err:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(os.EX_USAGE)

    verbose = False
    HOST = '127.0.0.1'
    PORT = 22
    USER = 'deploy'
    KEY_FILE = '~/.ssh/id_rsa'
    ENV = 'local'
    NAMESPACE = 'default'
    FILE = 'deploy/deployment.yml'
    TIMEOUT = 1
    for o, value in opts:
        if o == "-v":
            verbose = True
        elif o == "--help":
            usage()
            sys.exit(os.EX_OK)
        elif o == "-p":
            PORT = int(value)
        elif o == "-u":
            USER = value
        elif o == "-k":
            KEY_FILE = value
            print(KEY_FILE)
            if not os.path.isfile(KEY_FILE):
                print("Key file not found!")
                sys.exit(os.EX_NOINPUT)
        elif o == "-h":
            HOST = value
        elif o == "-n":
            NAMESPACE = value
        elif o == "-f":
            FILE = value
        elif o == "-t":
            TIMEOUT = value
        else:
            assert False, "unhandled option"

    c = Connection(HOST, port=PORT, user=USER,
                   connect_kwargs={"key_filename": KEY_FILE})
    deploy(c, FILE, NAMESPACE, TIMEOUT)
