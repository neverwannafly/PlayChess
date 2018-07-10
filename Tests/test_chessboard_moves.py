from .client import client
from .client import login

def test_legal_pawn_moves(client):
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
    # Add tests for enpassant later

def test_castling(client):
    login(client)
    # vestigial moves to clear away first rank to enable castling
    client.get('/makemove/e2-e4')
    client.get('/makemove/e7-e5')
    client.get('/makemove/g1-f3')
    client.get('/makemove/g8-f6')
