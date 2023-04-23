# Local Face

## Adding Valid Users

1. Add `.jpg` photos of valid users to the `valid_photoID` repository.
2. Modify the python dictionary in the `Detect.py` files to add a single dictionary entry for each user. Be sure to include the working directory path to the user photo/photos. Including multiple photos can increase detection reliability.

## Running the Program

### Raspberry Pi

1. Run `pip install -r piREQ.txt` or `pip3 install -r piREQ.txt` depending on your version of pip.
2. Run `python3 piDetect.py`.

### Mac

1. Run `pip install -r macREQ.txt` or `pip3 install -r macREQ.txt` depending on your version of pip.
2. Run `python3 piDetect.py`.
