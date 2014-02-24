# CS411 Team 1 Project #

## Required Software ##
- [Python v2.7.6][py]
- [Tornado v3.1.1][py-tornado]

## Additional Software ##
- [D3 v3.0][d3]
- [Twitter Bootstrap v3.0][bootstrap]

## Installation Instructions ##
There are two ways to install all the required dependencies for this
visualization:

- Manually through the use of a package manager (e.g. apt-get).
    - Run the command `sudo apt-get install python`.
    - Run the comment `sudo apt-get install python-tornado`.
- Automatically through the use of the Python installation tool [pip][].
    - Run the command `pip install -r .requirements.txt` from the
      base directory of the visualization source.

## Running Instructions ##
Once all the proper dependencies are installed, the project server can
be run using the command `make` from the base directory of the project.
The main page of the website can be viewed by opening a web browser and
entering the address [localhost:9999][localhost].

## Credits ##
Project originally developed as a course project for CS411 (Databases) 
at the University of Illinois Urbana-Champaign.

### Authors ###
- Eunsoo Roh (roh7)
- Joshua Halstead (halstea2)
- Thomas Bogue (tbogue2)
- Joseph Ciurej (ciurej2)


[py]: http://www.python.org/download/releases/2.7.6/ 
[pip]: http://www.tornadoweb.org/en/stable/
[py-tornado]: http://www.tornadoweb.org/en/stable/
[d3]: http://d3js.org/
[bootstrap]: http://getbootstrap.com/
[localhost]: http://localhost:9999
