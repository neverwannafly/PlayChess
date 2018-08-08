from flask import Blueprint, render_template, url_for, request, session, redirect, jsonify

mod = Blueprint('chat', __name__, template_folder='templates')