import kicad_script as k
from sexpdata import dumps, Symbol
from pprint import pprint


def test_create_board():
    board = k.create_board()
    assert board[0] == Symbol("kicad_pcb")


def test_get_thickness():
    board = k.create_board()
    assert k.get_thickness(board) == 1.6


def test_set_thickness():
    board = k.create_board()
    board = k.set_thickness(board, 1.7)
    assert k.get_thickness(board) == 1.7


def test_get_nets():
    board = k.create_board()
    [initial_net] = k.get_nets(board)
    assert initial_net.id == 0
    assert initial_net.name == ""


def test_add_nets():
    board = k.create_board()
    board = k.add_net(board, "Net 1")
    board = k.add_net(board, "Net 2")
    [initial_net, added_net_1, added_net_2] = k.get_nets(board)
    assert added_net_1.id == 1
    assert added_net_1.name == "Net 1"
    assert added_net_2.id == 2
    assert added_net_2.name == "Net 2"
