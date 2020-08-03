#implementing a robot obstacle avoidance algorithm

#import libraries
import simpleguitk as simplegui
import math
import random
import sys
sys.path.insert(0,'../')
sys.path.insert(0,'../')
import obavd3
import constants

#define globals

g_state = "None"


robot_co = 1


robot_pos=[337.135774033879, 308.1398152539053]
goal_pos=[343, 305]
full_obstacle_list=[(499, 180), (263, 7), (121, 333), (328, 233), (3, 424), (86, 173), (356, 275), (204, 426), (40, 231), (367, 38), (431, 304), (239, 349), (290, 363), (79, 283), (69, 166), (123, 265)]

start_pos = robot_pos

#create a sonar array

r1 = obavd3.Robot(robot_pos, robot_co, constants.N_SENSOR, goal_pos)

r1.update(full_obstacle_list, goal_pos)


def click(pos):
    global g_state, start_pos, goal_pos, robot_pos
    if g_state == "Start":
        start_pos = pos
        r1.set_pos(list(pos))
    elif g_state == "Goal":
        goal_pos = pos
        r1.set_co(obavd3.brg_in_deg(r1.get_pos(), pos))
    elif g_state == "Set Robot":
        r1.set_co(obavd3.brg_in_deg(r1.get_pos(), pos))
        r1.set_pos(list(pos))
        r1.delete_history()
    elif g_state == "Add Obs":
        full_obstacle_list.append(pos)
        print(full_obstacle_list)
        #update the robot
    r1.update(full_obstacle_list, goal_pos)
    g_state = "None"
        
def set_start():
    global g_state
    g_state = "Start"
    
def set_goal():
    global g_state
    g_state = "Goal"

def set_robot_pos():
    global g_state
    g_state = "Set Robot"

def alter_co(text):
    r1.set_co(float(text))
    r1.update()
            
def draw(canvas):
    # draw grids
    for x in range(0, constants.FRAME_SIZE, constants.SMALL_GRID_SIZE):
        canvas.draw_line((x, 0), (x, constants.FRAME_SIZE), 1, 'Gray')
    for y in range(0,constants.FRAME_SIZE,constants.SMALL_GRID_SIZE):
        canvas.draw_line((0, y), (constants.FRAME_SIZE, y), 1, 'Gray')

    #draw start 
    canvas.draw_circle(start_pos, 4, 3, "red")
    canvas.draw_text("S", [start_pos[0] + 10, start_pos[1] +10], 16, "red")
    #draw goal
    canvas.draw_circle(goal_pos, 4, 3, "green")
    canvas.draw_text("G", [goal_pos[0] + 10, goal_pos[1] +10], 16, "green")
    #draw the obstacles
    for obs in full_obstacle_list:
        canvas.draw_circle(obs,2,1, "red")
        canvas.draw_circle(obs, constants.OBSTACLE_RAD, 1, "white") 
    
    #draw sonar lines...
    r1.draw(canvas)

def step():
    r1.update()

def add_obs():
    global g_state
    g_state = "Add Obs"
    
    
#create simplegui controls

f1 = simplegui.create_frame("Obs Avoidance", constants.FRAME_SIZE, constants.FRAME_SIZE)
btn_start = f1.add_button("Set Start", set_start, 100)
btn_goal = f1.add_button("Set Goal", set_goal, 100)
btn_robot = f1.add_button("Set Robot", set_robot_pos, 100)
txt_r_co = f1.add_input("Robot Co", alter_co, 100)
btn_step = f1.add_button("Step", step, 100)
btn_add_obs = f1.add_button("Add Obs", add_obs, 100)

f1.set_draw_handler(draw)
f1.set_mouseclick_handler(click)

#start simplegui

f1.start()