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

### Logging
In the interest of complete transparency, there's an `audit.log` file generated
by default.  The console output only shows a certain amount of verbosity:

```
2015-11-03 11:18:08 - LotteryData - INFO - Entry['B']: 2
2015-11-03 11:18:08 - LotteryData - INFO - Entry['D']: 6
2015-11-03 11:18:08 - LotteryData - INFO - Entry['A']: 2
2015-11-03 11:18:08 - LotteryData - INFO - Entry['C']: 4
2015-11-03 11:18:08 - LotteryData - INFO - Picking 2 winners...
2015-11-03 11:18:08 - LotteryData - INFO - One prize per entry: Yes
2015-11-03 11:18:08 - LotteryData - INFO - Winner: <LotteryEntry name='D' weight=6>
2015-11-03 11:18:08 - LotteryData - INFO - Winner: <LotteryEntry name='A' weight=2>
2015-11-03 11:18:08 - draw.py - CRITICAL - Winners:
2015-11-03 11:18:08 - draw.py - CRITICAL - 1. D
2015-11-03 11:18:08 - draw.py - CRITICAL - 2. A
```

But the `audit.log` shows the whole process:

```
2015-11-03 11:18:08 - LotteryData - DEBUG - Reading from 'food_drive.csv'
2015-11-03 11:18:08 - LotteryData - DEBUG - Name column=2, weight columns=[3, 4]
2015-11-03 11:18:08 - LotteryData - DEBUG - Adding entry 'A', weight=1
2015-11-03 11:18:08 - LotteryData - DEBUG - Updating entry 'A', weight=1, net_weight=2
2015-11-03 11:18:08 - LotteryData - DEBUG - Adding entry 'B', weight=2
2015-11-03 11:18:08 - LotteryData - DEBUG - Adding entry 'C', weight=4
2015-11-03 11:18:08 - LotteryData - DEBUG - Adding entry 'D', weight=6
2015-11-03 11:18:08 - LotteryData - INFO - Entry['B']: 2
2015-11-03 11:18:08 - LotteryData - INFO - Entry['D']: 6
2015-11-03 11:18:08 - LotteryData - INFO - Entry['A']: 2
2015-11-03 11:18:08 - LotteryData - INFO - Entry['C']: 4
2015-11-03 11:18:08 - draw.py - DEBUG - Loaded 4 entries with total weight 14
2015-11-03 11:18:08 - LotteryData - INFO - Picking 2 winners...
2015-11-03 11:18:08 - LotteryData - INFO - One prize per entry: Yes
2015-11-03 11:18:08 - LotteryData - DEBUG - Weight Ring: [<LotteryEntry name='B' weight=2>, <LotteryEntry name='B' weight=2>, <LotteryEntry name='D' weight=6>, <LotteryEntry name='D' weight=6>, <LotteryEntry name='D' weight=6>, <LotteryEntry name='D' weight=6>, <LotteryEntry name='D' weight=6>, <LotteryEntry name='D' weight=6>, <LotteryEntry name='A' weight=2>, <LotteryEntry name='A' weight=2>, <LotteryEntry name='C' weight=4>, <LotteryEntry name='C' weight=4>, <LotteryEntry name='C' weight=4>, <LotteryEntry name='C' weight=4>]
2015-11-03 11:18:08 - LotteryData - INFO - Winner: <LotteryEntry name='D' weight=6>
2015-11-03 11:18:08 - LotteryData - DEBUG - 'D' already won once, picking again
2015-11-03 11:18:08 - LotteryData - INFO - Winner: <LotteryEntry name='A' weight=2>
2015-11-03 11:18:08 - draw.py - CRITICAL - Winners:
2015-11-03 11:18:08 - draw.py - CRITICAL - 1. D
2015-11-03 11:18:08 - draw.py - CRITICAL - 2. A
```

The above output was generated with a CSV of:

```
Timestamp,Username,Who is donating?,How much money are they donating?,How many food items are they donating?
now,admin,A,1,0
now,admin,A,,1
now,admin,B,1,1
now,admin,C,4,
now,admin,D,,6
```
