# Mazesolver
  <h4>maze_recursive.py</h4>
  The main driver file for simulation.
  
  <h4>maze_runner.py</h4>
  Class declaration and exploration logic declarations. <br>
  To change simulation settings, change the following:
  
  ```
  # Line 394 at maze_runner.py
  if __name__=='__main__':
    SIMULATION_SIZE = 20
    sim_x=15
    sim_y=10
    nagents=8
    gen_img=1
    ...
  ```
  <i>SIMULATION_SIZE</i> : number of testcases(maps)<br>
  <i>sim_x, sim_y</i> : size of map(width, height)<br>
  <i>nagents</i> : number of agents(multi-agent case)<br>
  <i>gen_img</i> : don't generate image GIFs if set to 0. Otherwise, generate GIF animations as output.
  
  ```
  class Robot():
    explore_left()
    broadcast()
    move()
    ...
  ```

  <h4>maze_map.py</h4>
  Class declaration of maze map structure.
  
  <h4>maze.py</h4>
  This file is not used.
