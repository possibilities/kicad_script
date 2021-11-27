import uuid
from sexpdata import loads, Symbol
from types import SimpleNamespace


def create_board():
    with open("./fixtures/initial.kicad_pcb") as f:
        initial = loads(f.read())
    return initial


def get_value(board, name):
    try:
        value = next(item for item in board if item[0] == Symbol(name))
        return value[1:]
    except Exception:
        return None


def set_value(board, name, value):
    def item_value(item):
        if isinstance(item, list) and str(item[0]) == name:
            return (item[0], value)
        else:
            return item

    return list(map(item_value, board))


timestampable_footprint_items = ["fp_text", "pad", "gr_line", "fp_line"]


def add_timestamps(item):
    if (isinstance(item, list) or isinstance(item, tuple)) and str(
        item[0]
    ) in timestampable_footprint_items:
        item = set_value(item, "tstamp", Symbol(uuid.uuid4()))
    return item


def add_footprint(board, options):
    position = options["position"]
    rotation = options["rotation"]
    library_name = options["library_name"]
    footprint_name = options["footprint_name"]

    with open(f"{library_name}.pretty/{footprint_name}.kicad_mod") as f:
        footprint_template = loads(f.read())

    at = [*position, rotation] if "rotation" in options else position

    footprint = [
        Symbol("footprint"),
        f"{library_name}:{footprint_name}",
        [Symbol("tstamp"), Symbol(uuid.uuid4())],
        [Symbol("at"), *at],
        *list(map(add_timestamps, footprint_template[2:])),
    ]

    return (*board, footprint)


def get_footprints(board):
    return [item for item in board if item[0] == Symbol("footprint")]


def get_thickness(board):
    general = next(item for item in board if item[0] == Symbol("general"))
    thickness = next(
        item for item in general if item[0] == Symbol("thickness")
    )
    return thickness[1]


def get_nets(board):
    return [
        SimpleNamespace(**{"id": item[1], "name": item[2]})
        for item in board
        if item[0] == Symbol("net")
    ]


def add_net(board, name):
    next_id = len(get_nets(board))
    return (*board, (Symbol("net"), next_id, name))


def set_edge_cut_points(board, points, width=0.1):
    return (
        *board,
        *[
            (
                Symbol("gr_line"),
                (Symbol("start"), point[0], point[1]),
                (
                    Symbol("end"),
                    points[index + 1 if index < (len(points) - 1) else 0][0],
                    points[index + 1 if index < (len(points) - 1) else 0][1],
                ),
                (Symbol("layer"), "Edge.Cuts"),
                (Symbol("width"), width),
                (Symbol("tstamp"), Symbol(uuid.uuid4())),
            )
            for index, point in enumerate(points)
        ],
    )


def get_edge_cut_points(board):
    return [
        item[1][1:]
        for item in board
        if item[0] == Symbol("gr_line") and item[3][1] == "Edge.Cuts"
    ]