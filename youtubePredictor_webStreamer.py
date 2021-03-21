


import json
import threading
import websocket




class Webstreamer():
    def __init__(self, speech_to_text_endpoint=None, speech_to_text_service=None, audio_source=None):
        self.speech_to_text_service = speech_to_text_service
        self._url = speech_to_text_endpoint
        self._ws = websocket.WebSocket(enable_multithread=True)


    def enter(self):

        def receive_messages():
            while True:
                msg = self._ws.recv()
                if not msg:
                    break
                data = json.loads(msg)
                self.output.put(data)

        self._ws.connect(self._url)
        self._ws.send(json.dumps(self.speech_to_text_service).encode('utf8'))
        result = json.loads(self._ws.recv())
        assert result['state'] == 'listening'

        t = threading.Thread(target=receive_messages)
        t.daemon = True  # Not passed to the constructor to support python 2
        t.start()

    def exit(self):
        self._ws.close()

    def consume(self, chunk):
        self._ws.send(chunk, websocket.ABNF.OPCODE_BINARY)