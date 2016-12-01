By Joey-Michael Fallone and Tony Qian 


We certify that all work contained here is our own work. 
Discussions about the project occurred with Reem Maarouf and Aaron Philips's
group, however all work was done separately. 


PLEASE NOTE THAT INPUT FILE SHOULD BE LABELED "input.txt" AND PLACED
IN THE ROOT DIRECTORY
THEN ./clean.sh MUST BE RUN

Phase 1: 
    To build the text files run: 
        cd p1  // move to the phase 1 dir

        ./make.sh // runs script to delete legacy files and create new ones

        cd .. // move back to main directory 

Phase 2:
    To sort and build the index files run:
        cd p2 // move to phase 2 dir

        ./build.sh // runs script

        cd .. // move back to main dir

Phase 3: 
    To run main program
    cd p3 // move into phase 3 dir

    python3 main.py // run program

    cd .. // move back to main dir

IF ANY BASH  SCRIPTS GIVE PERMISSION ERRORS RUN THE FOLLOWING:
    chmod + x name_of_problematic_script.sh
