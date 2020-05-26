from threading import Thread, Event

from arduinopythonserialrpc.arduino_python_serial_rpc import ArduinoPythonSerialRpc


class ArduinoController(ArduinoPythonSerialRpc):
    ''' ArduinoController extends ArduinoPythonSerialRpc this promote the Sketch inside Arduino Card as a
    potential caller of public methods implemented here (i.e. button) '''
    def __init__(self, port_name: str, baud_rate: int):
        super(ArduinoController, self).__init__(port_name, baud_rate, self)
        self.agent = AsyncStatusAgent(self)
        self.agent.start()

    def stop(self):
        ''' Disconnect from card and terminate the agent thread '''
        self.agent.disconnect()
        self.disconnect()

    def button(self, status: str) -> str:
        '''
        This method is the one specified into the Sketch as: arpc.executeRemoteMethod("button", "PRESSED");
        :param status: the value sent from the Sketch (i.e. "PRESSED")
        :return: A string returned to the Sketch. In this simple example it is ignored.
        '''
        print("Arduino says: Button is "+status)
        self._manage_status(status)
        return ""

    def _manage_status(self, status: str):
        '''
        Implements the simple activation business logic of embedded Arduino Led.
        This method call the Sketch registered function during the setup:
            arpc.registerArduinoFunction("LedUpdate", ledControl);
        :param status: the driving value
        '''
        if status == "PRESSED":
            self.agent.send_to_arduino("ON")
        else:
            self.agent.send_to_arduino("OFF")


ARDUINO_FUNCTION_TO_CALL = "LedUpdate"


class AsyncStatusAgent(Thread):
    def __init__(self, ar: ArduinoController):
        super(AsyncStatusAgent, self).__init__()
        self.daemon = True
        self.arduino = ar
        self.is_active = True
        self.status = None
        self.lock = Event()

    def disconnect(self):
        self.is_active = False
        self._ready_signal()  # Unlock the waitReadySignal inside run()

    def send_to_arduino(self, value: str):
        self.status = value
        self._ready_signal()
    
    def run(self):
        response = ''
        while self.is_active:
            if self._wait_ready_signal():
                self.lock.clear()
                if self.is_active:
                    try:
                        response = self.arduino.execute_remote_function(ARDUINO_FUNCTION_TO_CALL, self.status)
                    except Exception as ex:
                        print("Sorry, failure with Arduino card: " + str(ex))
                    print("Executed Led Switch number: " + response)

    def _wait_ready_signal(self) -> bool:
        return self.lock.wait(1000)

    def _ready_signal(self):
        self.lock.set()
