# Utility tools to manipulate stories

from .chessboard import Chessboard

class Story:
    pass

def loadStory(db_object, story_id):
    story = db_object.story.find_one({
        '_id': story_id,
    })
    return story

def deleteStory(db_object, story_id):
    db_object.story.delete_one({
        '_id': story_id,
    })

def addStory(db_object, username, board):
    story = board.get_states_as_json()
    story_id = db_object.story.insert_one(story)

    author = db_object.users.update_one(
        {"username": username},
        {"$push": {"story": story_id.inserted_id}},
    )

    return True if author.matched_count > 0 else False
