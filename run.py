#!/usr/bin/env python

from PlayChess import socketio, app, celery

if __name__ == '__main__':
    socketio.run(app)
