import csv
import sys
import tempfile


def rows_to_csv(rows, delimiter=',', quotechar='"'):
    """ Transform SQLite rows to CSV """

    # Open a temporary file
    with tempfile.NamedTemporaryFile('w+') as file_:
        # Write all rows to a temporary file
        wr = csv.writer(file_, delimiter=delimiter,
                        quotechar=quotechar, quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            wr.writerow(list(row))

        # Flush to actually write rows even if there is a pending buffer
        file_.flush()

        # Read finalized CSV
        with open(file_.name, 'r') as f:
            lines = f.read()

    return lines
