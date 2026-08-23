@echo off
cd /d "C:\Users\Marc Aradillas\Projects\Github-repos\Websites\FlowRootsWebsite\FlowRoots_App"
python -m waitress --host=0.0.0.0 --port=5000 main:app