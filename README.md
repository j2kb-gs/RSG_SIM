# RSG_SIM

1 Download and insatll webots R2022a. the installation procwedure can be found at https://cyberbotics.com/doc/guide/installation-procedure

## For windows
2- After installing webots, navigate to Tools-> Preference -> Python command. 
3- Make sure that it is pointing at `C:\Users\user\AppData\Local\Programs\Python\Python37\python.exe`
4- To run the simulation navigate to RSG_SIM -> worlds and double click on `soccer.wbt`

## Debugging
The following error may occur after opening the world file, 

`ERROR: 'C:/Users/badji/Downloads/J2KB/RSG_SIM/worlds/soccer.wbt':2:1: error: Expected node or PROTO name, found 'EXTERNPROTO'.
ERROR: 'C:/Users/badji/Downloads/J2KB/RSG_SIM/worlds/soccer.wbt': Failed to load due to syntax error(s).`

To fix it, open the `soccer.wbt` using vscode or any code editor and the delete the following two lines from the top of the file. 

`EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2022b/projects/objects/backgrounds/protos/TexturedBackground.proto"
EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2022b/projects/objects/backgrounds/protos/TexturedBackgroundLight.proto"`
