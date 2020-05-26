import sys

from arduinopythonserialrpctutorial.arduino_controller import ArduinoController

EXPECTED_SKETCH = "Led Tutorial Sketch (www.mauxilium.it)"


class PythonRpcTutorial:
    def __init__(self):
        pass

    def do_it(self, port_name: str, baud_rate: int):
        print("Hello from Mauxilium Arduino RPC Python Tutorial")
        ctrl = ArduinoController(port_name, baud_rate)
        ctrl.connect()

        card_name = ctrl.get_card_name()
        if EXPECTED_SKETCH == card_name:
            print("Connected to card: "+card_name)
        else:
            print("Invalid card. Found \""+card_name+"\" instead of expected \""+EXPECTED_SKETCH+"\"")
            ctrl.stop()
            exit(-1)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        tutorial = PythonRpcTutorial()
        tutorial.do_it(sys.argv[1], int(sys.argv[2]))
    else:
        print("\nPlease use: PythonRpcTutorial 'port' 'baudRate'")
        print("I.e.: PythonRpcTutorial COM5 9600")
