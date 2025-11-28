from pathlib import Path

from streamdeck_sdk_pi import *

OUTPUT_DIR = Path(__file__).parent
TEMPLATE = Path(__file__).parent / "pi_template.html"


def main():
    pi = PropertyInspector(
        action_uuid="nl.koenvh.screendeck.myaction",
        elements=[
            Message(
                uid="info_howto",
                heading="How it works",
                message_type=MessageTypes.INFO,
                text="Set this tile to all the tiles on your Stream Deck. It will automatically play the right video part on the right tile. You can add your own tiles too, the video will simply be missing there. Press once on any of the streaming tiles to start the video, and press again to stop the video. You may need to refresh the profile or page after making changes.",
            ),
            Message(
                uid="caution_tiles",
                heading="Using multiple tiles",
                message_type=MessageTypes.CAUTION,
                text="Set the stream URL only once! Setting multiple different stream URLs leads to undefined behaviour.",
            ),
            Textfield(
                label="Stream URL",
                uid="stream",
                required=False,
                placeholder="https://www.twitch.tv/Koenvh"
            ),
            Radio(
                label="Button role",
                uid="role",
                items=[
                    RadioItem(
                        value="Start/Stop",
                        label="Start/Stop",
                        checked=True,
                    ),
                    RadioItem(
                        value="Play/Pause",
                        label="Play/Pause",
                        checked=False,
                    ),
                    RadioItem(
                        value="Volume Up",
                        label="Volume Up",
                        checked=False,
                    ),
                    RadioItem(
                        value="Volume Down",
                        label="Volume Down",
                        checked=False,
                    ),
                ]
            )
        ]
    )
    pi.build(output_dir=OUTPUT_DIR, template=TEMPLATE)


if __name__ == '__main__':
    # Run to generate Property Inspector
    main()
