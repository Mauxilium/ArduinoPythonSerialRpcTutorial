import sys

from arduinopythonserialrpctutorial.python_rpc_tutorial import PythonRpcTutorial

if __name__ == "__main__":
    if len(sys.argv) == 3:
        tutorial = PythonRpcTutorial()
        tutorial.do_it(sys.argv[1], int(sys.argv[2]))
    else:
        print("\nPlease use: PythonRpcTutorial 'port' 'baudRate'")
        print("I.e.: PythonRpcTutorial COM5 9600")
        exit(-1)
