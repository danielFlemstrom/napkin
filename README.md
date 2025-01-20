# Wiping your T-EARS with NAPKIN
NAPKIN is a fork/continuation of the SCANIA+RISE project SAGA https://github.com/scania/saga.git <br> Napkin is currently(always) under heavy development. 

## Running Napkin Without Back-End Servers:

    sudo apt-get update
    sudo apt-get upgrade --yes
    sudo apt-get install git --yes
    git clone https://danielFlemstrom@bitbucket.org/danielFlemstrom/napkin.git

Double click on the file: `~/napkin/dist/index.html`     

## Preparing the Development Environment Container
Note, you need to have Docker installed on your local machine. <br>
From now on we decided to use a dockerized development environment since it is quite a lot of work to get all dependencies to work. 
The dependencies are specificed in two places: in the `<napkin>/Docker/pyproject.toml` and `<napkin>/client/package.json`.<br>
<hr>
On you local machine, prepare a source directory (the example uses /Users/dfm01/Documents/aProjects/napkincontainer)

Start with checking out the source there: 

    git clone git@bitbucket.org:danielFlemstrom/napkin.git

Build the development environment Docker container:<br>
In the root of the git repository:

     bash Docker/build-dev-container.sh

## Running the Development Environent Container:
The container does not contain any project specific data, instead you share the napkin git repo you cloned to your local harddrive. Depending on your local system (Windows/Linux/Mac) you may need to adjust the user id in `Docker/Dockerfile.development`, and/or your file permissions on your local machine via the Docker GUI. https://stackoverflow.com/questions/31448821/how-to-write-data-to-host-file-system-from-docker-container <br>
In your local machine in the `<napkin>` directory, start the container by:

    bash Docker/start-dev-container.sh

If you are running windows, look into the script and commit a BAT version. The command mounts the source directory on your harddrive so it is accessible inside the container. Now you can use e.g. vscode to edit the files in your local machine, and the changes are visible to the container. If you get an error message, there is probably some issues with the user "ubuntu" in the container accessing files in your local folder. 
The first time the container is started, it will install some npm packages (stored on your local mounted dir). 
Everytime, it needs to install the local python package from the source. 
A lot of warnings are issued because the versions are old. This should be fixed by someone...<br>
A default .env is also created if it does not already exist in the napkin git root. 

## Running The Development Server in the Development Environment Container
### Global project settings: 
There has to be a `session` directory that contains logs and g/a's.
Note that the back-end server needs to write to this directory, so it typically resides on the same level as the git repo (so it gets mounted properly when starting the container). The structure of that directory looks something like this.

        session
        ├── GA
        │   ├── SR_C30_SRS_Safe-REQ-244.txt
        ├── generated
        │   ├── ANALYSIS_overview.html
        ├── log
        │   ├── CXF1-2020-09-23_FrcEnPatched
        │   │   ├── 2_200_0_Passed_20200923_120418_TC-DriveBrake-S-001_SoftCCU_LOGDATA_20200923_120439_00.TXT
        │   │   ├── 2_200_0_Passed_20200923_121147_TC-DriveBrake-S-020_SoftCCU_LOGDATA_20200923_121207_00.TXT
        │   └── Expert-Sessions
        │       ├── LOGDATA_20201009_113748_2501_CCUO_A1_IP_80.TXT
        │       └── LOGDATA_20201009_120327_2501_CCUO_A1_IP_80.TXT
        ├── main_definitions.ga
        └── req


 This is located by the file `<napkin>/.env` that can adjusted if necessary. NOTE, that the paths are absolute and you should look inside the container NOT your local file system. NOTE also that you should NOT check in the `.env` file!
 If any errors are encountered, check in `example.end` instead.
## Starting the development servers:
In <napkin>/client:<br>

    npm run dev


# Misc Stuff Than May Be Useful Someday

For unknown reason, there is a npm_modules under 
`client/js/brace` as well. Probably only needed if you rebuild ace editor. A `npm install .`should do it if that is the case. 

 
        cd client/js
        node install .

 

# KARMA
* http://karma-runner.github.io/2.0/intro/installation.html
*  https://www.npmjs.com/package/karma-jasmine



# Must have doc links
* Debugging the grammar
https://ohmlang.github.io/editor/#30325d346a6e803cc35344ca218d8636


* The graphical elements used in the GUI:
* https://bootstrap-vue.js.org/
* https://gojs.net/latest/samples/sequenceDiagram.html



## TO BUILD A RELEASE:
In the project root:
 
    npm run build
 

Note that the produced file must be run in a web server in a structure like this:
 
        X-
        |- dist
            |- build.js
        |- index.html
 

index.html should contain the following:

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>gaeditorweb2.1</title>
        </head>
        <body>
            <div id="app"></div>
            <script src="dist/build.js"></script>
        </body>
        </html v>
 



# License and other information

This project as a whole is licensed by Scania CV AB under the GNU General
Public License version 3.0 or any later version. For the avoidance of doubt,
Scania CV AB holds the patent
SE540377 *Methodology for testing using interactively changed traces* which
is related to this project. Should this patent be seen as covering whole or
parts of this project, this patent is explicitly considered part of the
*essential patent claims* as per the license.


