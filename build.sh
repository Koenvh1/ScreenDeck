cd nl.koenvh.screendeck.sdPlugin/code
pyinstaller --noconfirm ./main.spec
cd ../..
streamdeck_sdk build -i nl.koenvh.screendeck.sdPlugin