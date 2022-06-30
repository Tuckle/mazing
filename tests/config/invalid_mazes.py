INVALID_MAZES = (
    ({
         "entrance": "A1", "gridSize": "8x8",
         "walls": ["C1", "G1", "A2", "C2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6",
                   "E6", "G6", "G7", "B8"]
     }, b"Maze does not have an unique exit point."),
    ({
        "entrance": "Z1", "gridSize": "7x8",
        "walls": ["C1"]
    }, b"Invalid entrance."),
    ({
        "entrance": "AB1", "gridSize": "8x8",
        "walls": ["C1"]
    }, b"Invalid entrance."),
    ({
        "entrance": "A1", "gridSize": "8x8",
        "walls": ["Z1"]
    }, b"Invalid wall."),
    ({
         "entrance": "-1", "gridSize": "8x8",
         "walls": ["A1"]
     }, b"Invalid entrance."),
    ({
         "entrance": "A1", "gridSize": "1x1",
         "walls": ["A1"]
     }, b"Invalid gridSize."),
    ({
         "entrance": "A1", "gridSize": "4x4",
         "walls": ["A3", "B3", "C3", "D3"]
     }, b"No valid path found in maze."),
)
