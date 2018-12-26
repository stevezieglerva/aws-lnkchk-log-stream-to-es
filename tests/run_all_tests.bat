cls

call ..\Scripts\activate
set text_logging=Y
call python -m unittest discover -s "." -p "*tests*.py"
call deactivate
