import re
import csv
import sys
import os

# for testing purposes
# filename_o = 'test_output.csv'
# filename = 'log2'

# use only if the log line starts with date
def multiline_parsing(filename):
    stitched_lines = []
    current_buffer = ""

    new_log_pattern = re.compile(r"^\[?\d{4}-\d{2}-\d{2}")

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue

            if new_log_pattern.match(line):
                if current_buffer:
                    stitched_lines.append(current_buffer)
                current_buffer = line
            else:
                current_buffer += " " + line

    if current_buffer:
        stitched_lines.append(current_buffer)

    return stitched_lines

def iterate_file(filename, filename_out, col_limit):
        lines = multiline_parsing(filename)
        # Uncomment and indent rest of the function when not using multiline_parsing
        # with open(filename, 'r', encoding='utf-8') as f:
        with open(filename_out, 'w', newline='', encoding='utf-8') as s:
            writer = csv.writer(s)

            for line in lines:
                pattern = r"(\[.*?\])|(\S+)"
                raw_matches = re.findall(pattern, line)
                clean_list = []

                for match in raw_matches:
                    token = match[0] if match[0] else match[1]

                    if len(token) > 1 or token.isalnum():
                        clean_list.append(token)

                if len(clean_list) > col_limit:
                    start = clean_list[:col_limit - 1]
                    end = " ".join(clean_list[col_limit - 1:])
                    clean_list = start + [end]

                if clean_list:
                    writer.writerow(clean_list)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Missing arguments. Usage: log_parser.py <input> <output> <limit>")
        print(f"Usage: log_parser.py <input> [output] [column_limit]")
        sys.exit(1)
    else:
        input_path = sys.argv[1]
        output_path = ""
        col_limit = 5

        if len(sys.argv) > 2:
            output_path = sys.argv[2]
            if output_path and not output_path.lower().endswith('.csv'):
                output_path += ".csv"

        if len(sys.argv) > 3:
            try:
                col_limit = int(sys.argv[3])
            except ValueError:
                print("Invalid limit provided. Using default: 5")
        if not output_path:
            folder = os.path.dirname(input_path)
            filename = os.path.basename(input_path)
            name_only, ext = os.path.splitext(filename)

            new_filename = f"{name_only}_parsed.csv"
            output_path = os.path.join(folder, new_filename)
            print(f"No output specified. Defaulting to: {output_path}")

        iterate_file(input_path, output_path, col_limit)

        print(f"File created at: {output_path}")