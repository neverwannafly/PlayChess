from .client import client
from .client import login, logout

def test_legal_pawn_moves(client):
    # Simple Pawn Moves
    login(client)
    pawn_e4 = client.get('/board/makemove/e2-e4')
    assert pawn_e4.status_code==200
    pawn_d5 = client.get('/board/makemove/d7-d5')
    assert pawn_d5.status_code==200
    pawn_capture = client.get('/board/makemove/e4-d5')
    assert pawn_capture.status_code==200
    corner_pawn_moves = [
        client.get('/board/makemove/h7-h5'),
        client.get('/board/makemove/h2-h4'),
        client.get('/board/makemove/a7-a5'),
        client.get('/board/makemove/a2-a4'),
    ]
    for test_case in corner_pawn_moves:
        assert test_case.status_code==200

    # Enpassant
    client.get('/board/makemove/c7-c5')
    client.get('/board/makemove/c2-c4')
    pawn_fail_ep = client.get('/board/makemove/d5-c6')
    assert b'"success":false' in pawn_fail_ep.data
    
    client.get('/board/makemove/e7-e5')
    pawn_succ_ep = client.get('/board/makemove/d5-e6')
    assert b'"success":true' in pawn_succ_ep.data

    # Pawn promotion
    client.get('/board/reset?fen=r1bqkbnr/pP3ppp/2n1p3/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5')
    client.get('/board/makemove/b7-a8-Q')
    client.get('/board/makemove/h7-h5')
    new_queen_move = client.get('/board/makemove/a8-c8')
    assert b'"success":true' in new_queen_move.data

def test_castling(client):
    login(client)
    # Check short castle
    client.get('/board/makemove/e2-e4')
    client.get('/board/makemove/e7-e5')
    client.get('/board/makemove/g1-f3')
    client.get('/board/makemove/g8-f6')
    client.get('/board/makemove/f1-c4')
    client.get('/board/makemove/f8-c5')
    white_castle = client.get('/board/makemove/e1-g1')
    black_castle = client.get('/board/makemove/e8-g8')
    assert b'"success":true' in white_castle.data
    assert b'"success":true' in black_castle.data
    logout(client)

    # Check long castle
    login(client)
    client.get('/board/makemove/d2-d4')
    client.get('/board/makemove/d7-d5')
    client.get('/board/makemove/b1-c3')
    client.get('/board/makemove/b8-c6')
    client.get('/board/makemove/c1-f4')
    client.get('/board/makemove/c8-f5')
    client.get('/board/makemove/d1-d2')
    client.get('/board/makemove/d8-d7')
    white_castle = client.get('/board/makemove/e1-c1')
    black_castle = client.get('/board/makemove/e8-c8')
    assert b'"success":true' in white_castle.data
    assert b'"success":true' in black_castle.data

    # No castling in check
    client.get('/board/reset?fen=rnbq1rk1/pppp1ppp/5n2/4p3/3PP3/2b2N2/PP2BPPP/RNBQK2R w KQ - 1 6')
    white_castle = client.get('/board/makemove/e1-g1')
    assert b'"success":false' in white_castle.data

    # No castling when obstacle in the way
    client.get('/board/reset?fen=rn1qkbnr/ppp1pppp/3p4/1b6/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 1 4')
    white_castle = client.get('/board/makemove/e1-g1')
    assert b'"success":false' in white_castle.data

    # Castling couldnt lead to king being in check
    client.get('/board/reset?fen=r1bqk1nr/ppp2ppp/2np4/2b1p3/2B1PP2/5N2/PPPP2PP/RNBQK2R w KQkq - 1 5')
    white_castle = client.get('/board/makemove/e1-g1')
    assert b'"success":false' in white_castle.data
    
def test_checks(client):
    login(client)
    client.get('/board/reset?fen=rn1qkb1r/ppp2Bpp/3p1n2/4N3/4P3/2N5/PPPP1PPP/R1BbK2R b KQkq - 1 6')
    king_move = client.get('/board/makemove/e8-e7')
    assert b'"success":true' in king_move.data

    client.get('/board/reset?fen=rn1qkbnr/ppp1pppp/3p4/1b6/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 1 4')
    king_move = client.get('/board/makemove/e1-e2')
    assert b'"success":false' in king_move.data

def test_fen_sanity(client):
    login(client)
    # Match with regex, should result in default board
    client.get('/board/reset?fen=abcd')
    pawn_move = client.get('/board/makemove/e2-e4')
    assert b'"success":true' in pawn_move.data

    # Try a valid fen and play some moves
    client.get('/board/reset?fen=rnb2rk1/pp1qppbp/2p2np1/3p4/2PP4/1PN1PNP1/PB3PBP/R2QK2R w KQ - 0 10')
    moves = [
        client.get('/board/makemove/c4-d5'),
        client.get('/board/makemove/f6-d5'),
        client.get('/board/makemove/c3-d5'),
        client.get('/board/makemove/d7-d5'),
        client.get('/board/makemove/e1-g1'),
    ]
    assertions = [b'"success":true' in move.data for move in moves]
    for clause in assertions:
        assert clause