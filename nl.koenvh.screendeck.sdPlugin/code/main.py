import base64
import io
import threading
import time

import streamlink
from PIL import Image
from ffpyplayer.player import MediaPlayer

import settings
from streamdeck_sdk import (
    StreamDeck,
    Action,
    events_received_objs,
)


class MyAction(Action):
    UUID = "nl.koenvh.screendeck.myaction"
    devices = {}
    contexts = []
    stream = None
    thread = None
    thread_id = None

    def request_settings(self):
        for c in self.contexts:
            self.get_settings(context=c["c"])

    def check_disconnect(self):
        if len(self.contexts) == 0 and self.thread:
            t = time.time()
            self.thread_id = t
            self.thread = None

    def on_did_receive_settings(self, obj: events_received_objs.DidReceiveSettings) -> None:
        if obj.payload.settings["stream"]:
            self.stream = obj.payload.settings["stream"]

    def on_device_did_connect(self, obj: events_received_objs.DeviceDidConnect) -> None:
        self.devices[obj.device] = {
            "columns": obj.deviceInfo.size.columns,
            "rows": obj.deviceInfo.size.rows
        }

    def on_device_did_disconnect(self, obj: events_received_objs.DeviceDidDisconnect) -> None:
        self.devices.pop(obj.device)
        self.contexts = [x for x in self.contexts if x["d"] != obj.device]
        self.check_disconnect()

    def on_will_appear(self, obj: events_received_objs.WillAppear) -> None:
        if obj.payload.coordinates:
            c = {
                "x": obj.payload.coordinates.column,
                "y": obj.payload.coordinates.row,
                "d": obj.device,
                "c": obj.context
            }
            self.contexts.append(c)
            print(c)

    def on_will_disappear(self, obj: events_received_objs.WillDisappear) -> None:
        self.contexts = [x for x in self.contexts if x["c"] != obj.context]
        self.check_disconnect()

    def on_key_down(self, obj: events_received_objs.KeyDown) -> None:
        self.request_settings()

        t = time.time()
        self.thread_id = t
        if self.thread:
            self.thread = None
        else:
            self.thread = threading.Thread(target=self.run, args=(t,), daemon=True)
            self.thread.start()

    def run(self, t):
        url = self.stream
        if not url:
            time.sleep(2)
            url = self.stream
        if not url:
            for c in self.contexts:
                self.show_alert(context=c["c"])
            return

        streams = streamlink.streams(url)
        if "480p" in streams:
            stream = streams["480p"]
        elif "360p" in streams:
            stream = streams["360p"]
        else:
            stream = streams["worst"]

        media = stream.to_url()
        ff_opts = {
            # "infbuf": False,
            "framedrop": True,
        }
        player = MediaPlayer(media, ff_opts=ff_opts)


        while t == self.thread_id:
            frame, val = player.get_frame()
            start = time.time()

            if val != 'eof':
                if frame is not None:
                    img, t2 = frame
                    frame2 = img.to_bytearray()[0]
                    w, h = img.get_size()
                    frame = Image.frombuffer("RGB", (w, h), frame2, 'raw', "RGB", 0, 1)
                else:
                    time.sleep(0.005)
                    continue
            else:
                break

            gap = 22

            resized_frame = {}
            min_x = min(c["x"] for c in self.contexts)
            min_y = min(c["y"] for c in self.contexts)
            max_x = max(c["x"] for c in self.contexts)
            max_y = max(c["y"] for c in self.contexts)

            for c in self.contexts:
                # d = self.devices.get(c["d"])
                # if not d:
                #     continue

                width = ((max_x - min_x + 1) * 72) + ((max_x - min_x) * gap)
                height = ((max_y - min_y + 1) * 72) + ((max_y - min_y) * gap)
                if (width, height) in resized_frame:
                    image = resized_frame[(width, height)]
                else:
                    image = frame.resize((width, height))
                    resized_frame[(width, height)] = image

                x = int((c["x"] - min_x) * (72 + gap))
                y = int((c["y"] - min_y) * (72 + gap))

                box = (x, y, x + 72, y + 72)
                cropped = image.crop(box)

                buffer = io.BytesIO()
                cropped.save(buffer, format="PNG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                img_base64 = f"data:image/png;base64,{img_base64}"

                self.set_image(c["c"], img_base64)

            elapsed = time.time() - start
            wait = val - elapsed
            if wait > 0:
                time.sleep(wait)

        player.close_player()


if __name__ == '__main__':
    StreamDeck(
        actions=[
            MyAction(),
        ],
        # debug=True,
        log_file=settings.LOG_FILE_PATH,
        log_level=settings.LOG_LEVEL,
        log_backup_count=1,
    ).run()
