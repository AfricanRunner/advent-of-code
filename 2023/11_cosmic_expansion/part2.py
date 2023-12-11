import sys


def get_empty_rows(image: list[list[str]]) -> list[bool]:
    rows = []
    for row in image:
        contains_galaxy = False
        for space in row:
            if space == '#':
                contains_galaxy = True
                break
        rows.append(not contains_galaxy)
    return rows


def get_empty_cols(image: list[list[str]]) -> list[bool]:
    cols = []
    for c in range(len(image[0])):
        contains_galaxy = False
        for r in range(len(image)):
            if image[r][c] == '#':
                contains_galaxy = True
                break
        cols.append(not contains_galaxy)
    return cols


def get_distances(empty_spaces: list[bool]) -> list[int]:
    distances = []
    total = 0
    for is_empty in empty_spaces:
        if is_empty:
            total += (1000000 - 1)
        distances.append(total)
        total += 1
    return distances


def get_taxicab_distance(start: tuple[int, int], end: tuple[int, int],
                         row_dists: list[int], col_dists: list[int]) -> int:
    start_row, start_col = start
    end_row, end_col = end
    start_row, end_row = min(start_row, end_row), max(start_row, end_row)
    start_col, end_col = min(start_col, end_col), max(start_col, end_col)
    row_dist = row_dists[end_row] - row_dists[start_row]
    col_dist = col_dists[end_col] - col_dists[start_col]
    return row_dist + col_dist


def main(input: list[str]):
    image = [[space for space in row] for row in input]
    empty_rows = get_empty_rows(image)
    empty_cols = get_empty_cols(image)
    row_dists = get_distances(empty_rows)
    col_dists = get_distances(empty_cols)

    galaxy_positions = []
    for r, row in enumerate(image):
        for c, space in enumerate(row):
            if space == '#':
                galaxy_positions.append((r, c))

    total = 0
    for i in range(len(galaxy_positions) - 1):
        for j in range(i + 1, len(galaxy_positions)):
            total += get_taxicab_distance(galaxy_positions[i],
                                          galaxy_positions[j], row_dists,
                                          col_dists)
    print(total)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Invalid arguments, expected input file.")
    input_file_path = sys.argv[1]
    with open(input_file_path) as input_file:
        input = [line.strip() for line in input_file.readlines()]
        main(input)
