# Food Drive *"Hat"*

Virtual *"hat"* to run a lottery to pick prizes for employees that have
contributed to the company food drive.

## Usage
### Data
Export the *responses* spreadsheet to `food_drive.csv`

### Virtualenv

```sh
virtualenv -p python3.4 venv
. venv/bin/activate
pip install -r requirements.txt
```

### Draw!
The drawing can be run in two different ways:

- **No Prize Limit**

    ```sh
    ./draw.py --prizes 5
    ```

- **One Prize Per Person**

    ```sh
    ./draw.py --prizes 5 --one-prize
    ```

### Advanced Drawing

```
This is the virtual hat for performing the weighted lottery

Usage:
    ./draw.py [options] (--prizes COUNT)
    ./draw.py [options] (--prizes COUNT) [--csv FILE] [--one-prize] [--name COLUMN] [--weight COLUMN]...

Options:
    -c, --csv FILE      Path to CSV data file (Default: food_drive.csv)
    -p, --prizes COUNT  Number of draws to be pulled from the lottery
    -1, --one-prize     Only allow someone to win a single prize
    --name COLUMN       Indicate what colum a name is in
    --weight COLUMN     Indicate what column the weights are in
```
