A ROS 2 Python package implementing a dual-node system: a controller node that publishes keyboard velocity commands to a TurtleBot3, and a monitor node that subscribes to and logs the robot's real-time movement states.

## 1. Step-by-Step Setup Instructions

To implement and run this project, we followed a structured development workflow to build, configure, and verify the package from scratch:

### Step 1: Initialize the Workspace
First, we set up the dedicated ROS 2 directory structure on our system by creating a new workspace (`turtlebot_controller`) with a source directory (`src`) to hold our packages, then navigated into it.

### Step 2: Create the ROS 2 Python Package
Inside the source directory, we generated ROS 2 Python package named `turtlebot_controller` using the `ament_python` build type.

### Step 3: Create the Node Source Files
We added the executable Python scripts for both nodes inside the package's inner directory:
1. **The Controller Node (Publisher):** Responsible for capturing user keyboard inputs (`w`, `a`, `s`, `d`, `q`) and translating them into velocity commands.
2. **The Monitor Node (Subscriber):** Responsible for listening to the published velocity topics and outputting the real-time state of the robot.

### Step 4: Configure the Build Entry Points (`setup.py`)
To make both Python scripts executable as native ROS 2 nodes, we registered them inside the `setup.py` configuration file. We mapped the node names (`turtlebot_controller` and `turtlebot_monitor`) to their respective main functions.

### Step 5: Declare Package Dependencies (`package.xml`)
We updated the `package.xml` file to ensure the build system knows our package relies on the ROS 2 Python client library (`rclpy`) and the standard 3D velocity message package (`geometry_msgs`).

### Step 6: Build and Source the Workspace
We compiled the entire workspace from the root folder to generate the executable binaries. Once built, we sourced the workspace setup files to make the newly created package discoverable in our active terminal session.

### Step 7: Pre-Flight Verification and Run
Before running the nodes, we verified that the necessary communication topics were active and correctly configured. Finally, we launched both nodes in separate sourced terminal windows to establish real-time control and monitoring.

### Step 8: Run and Execute
Finally, we run the nodes simultaneously in separate terminal sessions. The Controller node is launched in one window to capture keyboard inputs, while the Monitor node is launched in another to capture and print the live feedback. 
When you press the control keys, the robot responds dynamically, and the monitor immediately prints the updated velocities, proving that the publisher-subscriber loop is successfully closed.
____________________________________________________________________________________________________________________________________________
## 2. Linux Commands Used and Their Functions

| Command | What It Does (Function) |
| `mkdir -p` | Creates a new directory and any missing parent folders. |
| `cd` | Changes the current working directory to a new path. |
| `pwd` | Prints the absolute path of the current working directory. |
| `nano` | Opens a simple terminal text editor to write or edit code files. |
_______________________________________________________________________________________________________________________________________
## 3. ROS 2 Commands Used and Their Functions

 1. Package Creation- create ros2 package we will work on with python build type
```bash
ros2 pkg create --build-type ament_python turtlebot_controller
```
2: Configure Node Code- craete our publisher node and subscriber node & putting python code through
```bash
nano ~/workspaces/turtlebot_controller/src/turtlebot_controller/turtlebot_controller/turtlebot_controller_node.py
nano ~/workspaces/turtlebot_controller/src/turtlebot_controller/turtlebot_controller/turtlebot_monitor_node.py
```
3: Update Package Configuration- we need to update the entry point to tell ROS 2 which Python file should run when we execute our node
```bash
nano ~/workspaces/turtlebot_controller/src/turtlebot_controller/setup.py
```
4: Build Workspace-Compiles and builds all packages in the workspace, generating the executable files
```bash
colcon build --packages-select turtlebot_controller
```
5-source-Registers the compiled packages in the active terminal so ROS 2 can find and run your nodes
```bash
source install/setup.bash
```
6-Launch Controller- run our programm - publisher & subscriber nodes
```bash- publisher run
ros2 run turtlebot_controller turtlebot_controller
```
```bash- subscriber run
ros2 run turtlebot_controller turtlebot_monitor
```
__________________________________________________________________________________
### 4- How to test your nodes 
 testing nodes through Pre-Flight Verification commands 
 ```bash
# Verify topics are available
ros2 topic list | grep -E "cmd_vel"

# Check /cmd_vel details
ros2 topic info -v /cmd_vel
```
____________________________________________________________________________________-
### 5. Expected Output
1-When you run the complete system and press the control keys in the publisher terminal, 
the expected output is :

The TurtleBot3 robot inside thesimulator changes its state from a standstill to active movement
according to the presses key:
W: move forward
A:move left
S: backward
D: right
Q: stop and exit

2- Expected Output in monitor terminal 
In the Monitor Node terminal (Subscriber), you will see a live, continuous stream
of logs printing the exact velocity values being received. The output looks like this:
 ```bash
[INFO] [turtlebot_monitor]: Receiving - Linear Vel: 0.2 m/s, Angular Vel: 0.0 rad/s
[INFO] [turtlebot_monitor]: Receiving - Linear Vel: 0.2 m/s, Angular Vel: 1.0 rad/s
[INFO] [turtlebot_monitor]: Receiving - Linear Vel: 0.0 m/s, Angular Vel: 0.0 rad/s (Stop)
```
____________________________________________________________________________________

## 6. Simulation Demo
 Simulation Demo: Speed TuningTo prevent the TurtleBot3 from flipping over and losing control in the simulation, we tuned down the velocity limits to match the robot's
 actual hardware constraints.What changed:Before (Unsafe): 0.5 m/s Linear | 1.0 rad/s Angular $\rightarrow$ The robot aggressively flips over due to 
 sudden acceleration.After (Safe): 0.15 m/s Linear | 0.5 rad/s Angular $\rightarrow$ Smooth, stable, and highly controlled movement.
 Watch the side-by-side demo below to see the difference in stability:

 ##FIRST VELOCITY: 
https://github.com/user-attachments/assets/e9557c1f-7b67-47c5-81cf-857010bae363

##SECOND VELOCITY{final}


https://github.com/user-attachments/assets/da0071d1-7a26-47da-8bb8-46a4326bff9c









 







