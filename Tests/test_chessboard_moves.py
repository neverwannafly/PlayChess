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

def test_checkmate(client):
    login(client)
    client.get("/board/reset?fen=r1bqk1nr/pppp1Qpp/2n5/2b1p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 1 4")
    black_move = client.get("/board/makemove/e8-f7")
    assert b'"gameFinished":true,"result":1' in black_move.data

def test_stalemate(client):
    login(client)
    client.get("/board/reset?fen=5k2/R3R3/8/2P2P2/6Q1/1P3N2/5P1K/2B5 b - - 1 27")
    black_move = client.get("/board/makemove/f8-d7")
    assert b'"gameFinished":true,"result":0.5' in black_move.data

def test_full_game(client):
    login(client)
    # The following game is played b/w Paul Morphy and Duke Karl
    m1 = client.get("/board/makemove/e2-e4")  #1
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"' in FEN.data
    m2 = client.get("/board/makemove/e7-e5")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"' in FEN.data
    m3 = client.get("/board/makemove/g1-f3")  #2
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"' in FEN.data
    m4 = client.get("/board/makemove/d7-d6")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rnbqkbnr/ppp2ppp/3p4/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3"' in FEN.data
    m5 = client.get("/board/makemove/d2-d4")  #3
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rnbqkbnr/ppp2ppp/3p4/4p3/3PP3/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 3"' in FEN.data
    m6 = client.get("/board/makemove/c8-g4")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn1qkbnr/ppp2ppp/3p4/4p3/3PP1b1/5N2/PPP2PPP/RNBQKB1R w KQkq - 1 4"' in FEN.data
    m7 = client.get("/board/makemove/d4-e5")  #4
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn1qkbnr/ppp2ppp/3p4/4P3/4P1b1/5N2/PPP2PPP/RNBQKB1R b KQkq - 0 4"' in FEN.data
    m8 = client.get("/board/makemove/g4-f3")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn1qkbnr/ppp2ppp/3p4/4P3/4P3/5b2/PPP2PPP/RNBQKB1R w KQkq - 0 5"' in FEN.data
    m9 = client.get("/board/makemove/d1-f3")  #5
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn1qkbnr/ppp2ppp/3p4/4P3/4P3/5Q2/PPP2PPP/RNB1KB1R b KQkq - 0 5"' in FEN.data
    m10 = client.get("/board/makemove/d6-e5")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn1qkbnr/ppp2ppp/8/4p3/4P3/5Q2/PPP2PPP/RNB1KB1R w KQkq - 0 6"' in FEN.data
    m11 = client.get("/board/makemove/f1-c4") #6
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn1qkbnr/ppp2ppp/8/4p3/2B1P3/5Q2/PPP2PPP/RNB1K2R b KQkq - 1 6"' in FEN.data
    m12 = client.get("/board/makemove/g8-f6")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn1qkb1r/ppp2ppp/5n2/4p3/2B1P3/5Q2/PPP2PPP/RNB1K2R w KQkq - 2 7"' in FEN.data
    m13 = client.get("/board/makemove/f3-b3") #7
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn1qkb1r/ppp2ppp/5n2/4p3/2B1P3/1Q6/PPP2PPP/RNB1K2R b KQkq - 3 7"' in FEN.data
    m14 = client.get("/board/makemove/d8-e7")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn2kb1r/ppp1qppp/5n2/4p3/2B1P3/1Q6/PPP2PPP/RNB1K2R w KQkq - 4 8"' in FEN.data
    m15 = client.get("/board/makemove/b1-c3") #8
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn2kb1r/ppp1qppp/5n2/4p3/2B1P3/1QN5/PPP2PPP/R1B1K2R b KQkq - 5 8"' in FEN.data
    m16 = client.get("/board/makemove/c7-c6")  
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn2kb1r/pp2qppp/2p2n2/4p3/2B1P3/1QN5/PPP2PPP/R1B1K2R w KQkq - 0 9"' in FEN.data
    m17 = client.get("/board/makemove/c1-g5") #9
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn2kb1r/pp2qppp/2p2n2/4p1B1/2B1P3/1QN5/PPP2PPP/R3K2R b KQkq - 1 9"' in FEN.data
    m18 = client.get("/board/makemove/b7-b5")  
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn2kb1r/p3qppp/2p2n2/1p2p1B1/2B1P3/1QN5/PPP2PPP/R3K2R w KQkq - 0 10"' in FEN.data
    m19 = client.get("/board/makemove/c3-b5") #10
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn2kb1r/p3qppp/2p2n2/1N2p1B1/2B1P3/1Q6/PPP2PPP/R3K2R b KQkq - 0 10"' in FEN.data
    m20 = client.get("/board/makemove/c6-b5") 
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn2kb1r/p3qppp/5n2/1p2p1B1/2B1P3/1Q6/PPP2PPP/R3K2R w KQkq - 0 11"' in FEN.data
    m21 = client.get("/board/makemove/c4-b5") #11
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"rn2kb1r/p3qppp/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/R3K2R b KQkq - 0 11"' in FEN.data
    m22 = client.get("/board/makemove/b8-d7")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"r3kb1r/p2nqppp/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/R3K2R w KQkq - 1 12"' in FEN.data
    m23 = client.get("/board/makemove/e1-c1") #12
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"r3kb1r/p2nqppp/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/2KR3R b kq - 2 12"' in FEN.data
    m24 = client.get("/board/makemove/a8-d8")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"3rkb1r/p2nqppp/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/2KR3R w k - 3 13"' in FEN.data
    m25 = client.get("/board/makemove/d1-d7") #13
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"3rkb1r/p2Rqppp/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/2K4R b k - 0 13"' in FEN.data
    m26 = client.get("/board/makemove/d8-d7")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"4kb1r/p2rqppp/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/2K4R w k - 0 14"' in FEN.data
    m27 = client.get("/board/makemove/h1-d1") #14
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"4kb1r/p2rqppp/5n2/1B2p1B1/4P3/1Q6/PPP2PPP/2KR4 b k - 1 14"' in FEN.data
    m28 = client.get("/board/makemove/e7-e6")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"4kb1r/p2r1ppp/4qn2/1B2p1B1/4P3/1Q6/PPP2PPP/2KR4 w k - 2 15"' in FEN.data
    m29 = client.get("/board/makemove/b5-d7") #15
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"4kb1r/p2B1ppp/4qn2/4p1B1/4P3/1Q6/PPP2PPP/2KR4 b k - 0 15"' in FEN.data
    m30 = client.get("/board/makemove/f6-d7")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"4kb1r/p2n1ppp/4q3/4p1B1/4P3/1Q6/PPP2PPP/2KR4 w k - 0 16"' in FEN.data
    m31 = client.get("/board/makemove/b3-b8") #16
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"1Q2kb1r/p2n1ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 b k - 1 16"' in FEN.data
    m32 = client.get("/board/makemove/d7-b8")
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"1n2kb1r/p4ppp/4q3/4p1B1/4P3/8/PPP2PPP/2KR4 w k - 0 17"' in FEN.data
    m33 = client.get("/board/makemove/d1-d8") #17 : Checkmate
    FEN = client.get("/board/generateFenNotation")
    assert b'"notation":"1n1Rkb1r/p4ppp/4q3/4p1B1/4P3/8/PPP2PPP/2K5 b k - 1 17"' in FEN.data

    status = client.get("/board/getGameStatus")
    assert b'"status":"finished","result":"1"' in status.data