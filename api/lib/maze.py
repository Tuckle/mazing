import collections


class InvalidMazeException(Exception):
    pass


def solve_maze(entrance, grid_size, walls):
    """
    Compute longest and shortest paths through given maze.
    :param entrance: Starting point in maze, e.g. A1
    :param grid_size: width and height of the maze separated by 'x', e.g. 8x8
    :param walls:
    :return:
    """
    # check validity of parameters
    try:
        width, height = list(map(int, grid_size.split('x')))
    except ValueError:
        raise InvalidMazeException("Invalid gridSize")
    try:
        start_from = (ord(entrance[0]) - 64, int(entrance[1:]))
    except ValueError:
        raise InvalidMazeException("Invalid entrance.")
    try:
        walls = set(map(lambda x: (ord(x[0]) - 64, int(x[1:])), walls))
    except ValueError:
        raise InvalidMazeException("Invalid wall.")
    try:
        assert width + height > 2 and width > 0 and height > 0, "Invalid gridSize."
        assert 1 <= start_from[0] <= width, "Invalid entrance."
        assert 1 <= start_from[1] <= height, "Invalid entrance."
        for wall in walls:
            assert 1 <= wall[0] <= width, "Invalid wall."
    except AssertionError as aer:
        raise InvalidMazeException(str(aer))

    queue = collections.deque()
    path_ = [start_from]
    visited_ = set()
    visited_.add(start_from)
    queue.append((path_.copy(), visited_))  # path, visited locations set for this path
    exits = set()
    min_len = width * height
    max_len = 0
    min_path = max_path = None

    while queue:
        path, visited = queue.popleft()
        x, y = path[-1]
        if y >= height:  # end of the line, completed path
            if len(path) < min_len:
                min_len = len(path)
                min_path = path.copy()
            elif len(path) > max_len:
                max_len = len(path)
                max_path = path.copy()
            exits.add(path[-1])

            if len(exits) > 1:  # maze not allowed to have multiple valid exit points
                raise InvalidMazeException("Maze does not have an unique exit point.")
            continue

        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            point = (x2, y2)
            if (0 < x2 <= width and  # X-axis in range
                    0 < y2 <= height and  # y-axis
                    point not in walls and  # not a wall
                    point not in visited):
                new_path = path.copy()
                new_path.append(point)
                new_visited = visited.copy()
                new_visited.add(point)
                queue.append((new_path, new_visited))
    if min_path:
        min_path = list(map(lambda x: "{}{}".format(
            chr(x[0] + 64), x[1]
        ), min_path))
    if max_path:
        max_path = list(map(lambda x: "{}{}".format(
            chr(x[0] + 64), x[1]
        ), max_path))
    if not min_path and not max_path:
        raise InvalidMazeException("No valid path found in maze.")

    return min_path, max_path


if __name__ == '__main__':
    print(solve_maze(
        "A1", "8x8",
        ["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6", "E6",
         "G6", "H6", "B7", "D7", "G7", "B8"]
    ))
