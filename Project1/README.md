# Project 1: Hex AI

## Objective
Create an Agent, based on the search algorithms reviewed on the course
"ST0273 - Ingeniría del Conocimiento" from "Universidad EAFIT",
capable of playing HEX and get the best possible performance at execution
time, so that each move a player does takes less than five (5) seconds, 
this agent will use Dijsktra as the evaluation method to get the best path
and get the best move always.

## General information
To run this game you will need jupyter as the main method to run the map
inside the map there is a function to call each player agent in order to
be succesfully call the agent code must be call by this way: 
Agent\_Name1\_Name2 then pass the player number and the current
game state in order to make the Agent do the best moves

### Execution requirements
* Python 3
* Jupyter
* copy library
* heapq library

### Who are involved?
* Tomás Felipe Llano Ríos
* Mateo Gutiérrez Gómez

### How to call the agent from Jupyther?
* Add the line:
  ```
  from Agente_Tomas_Mateo import Agente_Tomas_Mateo
  ```
* Call the agent by adding the line:
  ```
  Agente_Tomas_Mateo(state, player_number)
  ```
