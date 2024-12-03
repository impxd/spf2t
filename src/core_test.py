from core import Down, Left, Right, Up, edge, equalBlocks


def testEdgeShouldReturnCorrectEdgeForUpDirection():
    assert equalBlocks(edge([(4, 1), (4, 0)], Up()), [(4, 0)])
    assert equalBlocks(edge([(2, 1), (1, 1)], Up()), [(2, 1), (1, 1)])
    assert equalBlocks(edge([(3, 1), (3, 2)], Up()), [(3, 1)])
    assert equalBlocks(edge([(2, 2), (3, 2)], Up()), [(2, 2), (3, 2)])
    assert equalBlocks(edge([(3, 1), (3, 0)], Up()), [(3, 0)])


def testEdgeShouldReturnCorrectEdgeForDownDirection():
    assert equalBlocks(edge([(4, 1), (4, 0)], Down()), [(4, 1)])
    assert equalBlocks(edge([(2, 1), (1, 1)], Down()), [(2, 1), (1, 1)])
    assert equalBlocks(edge([(3, 1), (3, 2)], Down()), [(3, 2)])
    assert equalBlocks(edge([(2, 2), (3, 2)], Down()), [(2, 2), (3, 2)])


def testEdgeShouldReturnCorrectEdgeForRightDirection():
    assert equalBlocks(edge([(4, 1), (4, 0)], Right()), [(4, 1), (4, 0)])
    assert equalBlocks(edge([(2, 1), (1, 1)], Right()), [(2, 1)])
    assert equalBlocks(edge([(3, 1), (3, 2)], Right()), [(3, 1), (3, 2)])
    assert equalBlocks(edge([(2, 2), (3, 2)], Right()), [(3, 2)])


def testEdgeShouldReturnCorrectEdgeForLeftDirection():
    assert equalBlocks(edge([(4, 1), (4, 0)], Left()), [(4, 1), (4, 0)])
    assert equalBlocks(edge([(2, 1), (1, 1)], Left()), [(1, 1)])
    assert equalBlocks(edge([(3, 1), (3, 2)], Left()), [(3, 1), (3, 2)])
    assert equalBlocks(edge([(2, 2), (3, 2)], Left()), [(2, 2)])
