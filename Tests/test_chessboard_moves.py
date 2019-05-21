from .client import client
from .client import login, logout

def test_legal_pawn_moves(client):
    # Simple Pawn Moves
    login(client)
    pawn_e4 = client.get('/makemove/e2-e4')
    assert pawn_e4.status_code==200
    pawn_d5 = client.get('/makemove/d7-d5')
    assert pawn_d5.status_code==200
    pawn_capture = client.get('/makemove/e4-d5')
    assert pawn_capture.status_code==200
    corner_pawn_moves = [
        client.get('/makemove/h7-h5'),
        client.get('/makemove/h2-h4'),
        client.get('/makemove/a7-a5'),
        client.get('/makemove/a2-a4'),
    ]
    for test_case in corner_pawn_moves:
        assert test_case.status_code==200

    # Enpassant
    client.get('/makemove/c7-c5')
    client.get('/makemove/c2-c4')
    pawn_fail_ep = client.get('/makemove/d5-c6')
    assert b'"success":false' in pawn_fail_ep.data
    
    client.get('/makemove/e7-e5')
    pawn_succ_ep = client.get('/makemove/d5-e6')
    assert b'"success":true' in pawn_succ_ep.data

def test_castling(client):
    login(client)
    # Check short castle
    client.get('/makemove/e2-e4')
    client.get('/makemove/e7-e5')
    client.get('/makemove/g1-f3')
    client.get('/makemove/g8-f6')
    client.get('/makemove/f1-c4')
    client.get('/makemove/f8-c5')
    white_castle = client.get('/makemove/e1-g1')
    black_castle = client.get('/makemove/e8-g8')
    assert b'"success":true' in white_castle.data
    assert b'"success":true' in black_castle.data
    logout(client)

    # Check long castle
    login(client)
    