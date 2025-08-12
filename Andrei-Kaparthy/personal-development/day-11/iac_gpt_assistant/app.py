import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from iac_assistant import process_iac_request

load_dotenv
