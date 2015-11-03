#!/usr/bin/env python
"""

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
"""
import csv
import logging
import random
from util import LogProducer
from util import setup_logging

__version__ = "0.0"

setup_logging()

DEFAULT_CSV = "food_drive.csv"
DEFAULT_COLUMN_NAME = 2
DEFAULT_COLUMN_WEIGHT = [3, 4]


class LotteryEntry(object):
    def __init__(self, name, weight=0):
        self.name = str(name)
        self.weight = int(weight)

        assert len(self.name), \
            "Name must be a non-empty string"

    def add_weight(self, weight):
        try:
            self.weight += int(weight)
        except ValueError:
            pass

    def __int__(self):
        return self.weight

    def __repr__(self):
        return "<{cls} name='{name}' weight={weight}>".format(
            cls=self.__class__.__name__,
            name=self.name,
            weight=self.weight
        )

    def __str__(self):
        return self.name


class LotteryWinner(object):
    def __init__(self, entry):
        self.entry = entry

    @property
    def name(self):
        return self.entry.name

    @property
    def weight(self):
        return self.entry.weight

    def __repr__(self):
        return repr(self.entry)

    def __str__(self):
        return repr(self)


class LotteryData(LogProducer):
    @classmethod
    def from_csv(cls, file, name_column, weight_columns, has_header=True):
        # Ensure the column designations are all integers
        name_column = int(name_column)
        weight_columns = [int(x) for x in weight_columns]

        log = logging.getLogger(cls.__name__)
        log.debug("Reading from '{file}'".format(file=file))
        log.debug("Name column={namecol}, weight columns={weightcols}".format(
            namecol=name_column,
            weightcols=weight_columns
        ))

        data = cls()
        with open(file, "r") as input_file:
            reader = csv.reader(input_file)
            row_index = -1
            for row in reader:
                row_index += 1

                if row_index == 0 and has_header:
                    # Skip header
                    continue

                entry = LotteryEntry(row[name_column])
                for col in weight_columns:
                    entry.add_weight(row[col])

                data.add_entry(entry)

        data.log_entries()
        return data

    def __init__(self):
        LogProducer.__init__(self)
        self._entries = {}

    def add_entry(self, lottery_entry):
        assert lottery_entry.weight > 0, \
            "Entries must have a positive weight"

        if lottery_entry.name in self._entries:
            # This name already exists in the lottery, add weight
            self._log.debug(
                "Updating entry '{name}', weight={weight}"
                ", net_weight={netweight}".format(
                    name=lottery_entry.name,
                    weight=lottery_entry.weight,
                    netweight=(lottery_entry.weight +
                               self._entries[lottery_entry.name].weight)
                ))
            self._entries[lottery_entry.name].add_weight(lottery_entry.weight)

        else:
            # This name DOES NOT exist in the lottery, add it
            self._log.debug("Adding entry '{name}', weight={weight}".format(
                name=lottery_entry.name,
                weight=lottery_entry.weight
            ))
            self._entries[lottery_entry.name] = lottery_entry

        return self

    def draw(self, count, one_prize_only=False):
        if one_prize_only:
            assert count <= len(self._entries), \
                "Must have more entries than prizes if one-prize-per-entry"

        self._log.info("Picking {c} winner{s}...".format(
            c=count,
            s="s" if count > 1 else ""
        ))
        self._log.info("One prize per entry: {one_prize}".format(
            one_prize="Yes" if one_prize_only else "No"
        ))

        weight_ring = self._generate_weight_ring()
        self._log.debug("Weight Ring: {ring}".format(ring=weight_ring))
        winners = []
        winner_names = []

        weight_size = self.entry_weight
        for prize_num in range(count):
            while True:
                entry = random.choice(weight_ring)

                if one_prize_only and entry.name in winner_names:
                    # This entry cannot win another prize
                    self._log.debug(
                        "'{n}' already won once, picking again".format(
                            n=entry.name
                        ))
                    continue

                winning_entry = LotteryWinner(entry)
                self._log.info("Winner: {winner}".format(winner=winning_entry))
                winners.append(winning_entry)
                winner_names.append(winning_entry.name)
                break

        return winners

    @property
    def entry_count(self):
        return len(self._entries)

    @property
    def entry_weight(self):
        total_weight = 0
        for name, entry in self._entries.items():
            total_weight += entry.weight
        return total_weight

    def _generate_weight_ring(self):
        weight_ring = []
        for name, entry in self._entries.items():
            for i in range(entry.weight):
                weight_ring.append(entry)

        return weight_ring

    def log_entries(self):
        for name, entry in self._entries.items():
            self._log.info("Entry['{n}']: {w}".format(
                n=entry.name,
                w=entry.weight
            ))


if __name__ == '__main__':
    from docopt import docopt
    args = docopt(__doc__, version=__version__)

    try:
        args['--prizes'] = int(args['--prizes'])
    except ValueError:
        raise AssertionError("--prizes must be an integer")

    assert args['--prizes'] > 0, \
        "--prizes must be greater than zero"

    if not args['--csv']:
        args['--csv'] = DEFAULT_CSV

    if not args['--name']:
        args['--name'] = DEFAULT_COLUMN_NAME

    if not args['--weight']:
        args['--weight'] = DEFAULT_COLUMN_WEIGHT

    log = logging.getLogger("draw.py")
    data = LotteryData.from_csv(
        args['--csv'],
        args['--name'],
        args['--weight']
    )
    log.debug("Loaded {c} entries with total weight {w}".format(
        c=data.entry_count,
        w=data.entry_weight
    ))

    winners = data.draw(args['--prizes'], args['--one-prize'])
