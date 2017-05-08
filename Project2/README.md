# Project 2: Estrellita Donde Estas AI

## Objective
Create an Agent, based on the Markov-Models inference algorithms
reviewed on the course "ST0273 - Ingeniería del Conocimiento" 
from "Universidad EAFIT", capable of playing "Estrellita Donde Estas" 
This agent will use HMM (Hidden Markov Models) as the evaluation method 
to determine the best shooting position and obtain the best move 
to execute by using the "determine\_move\_position" function.

### Execution requirements
* Python 3
* numpy
* Jupyter

### Who are involved?
* Tomás Felipe Llano Ríos
* Mateo Gutiérrez Gómez

### How to call the agent from Jupyter?
* Add the line:
  ```
  from agent_none import AgentNone
  ```
* Instance the agent by adding the line:
  ```
  agent_none = AgentNone()
  ```
* Call the agent by adding the line:
  ```
  agent_none.run_agent_none(<current_player>, <our_result>, <enemy_action>, <init_pos>)
  ```
