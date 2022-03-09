#!/usr/bin/env python3

import subprocess
import time
import sys

output = ""

# State Machine loop
# Not totally a state machine since there are globals, but pretty close
def stateMachine(state):
    while True:
        # call the current state, and update with the next state
        #print (state)
        state = state()

        # It should be ok to keep this pretty low since in most cases, the
        # program will generate the same output and do very little work
        #time.sleep(0.1)

def updateState():
    # run the build process, in this case, "make"
    result = subprocess.run(['make', '-q'])

    # if make -q returns 1, the build needs to be updated
    if result.returncode == 1:
        return buildState

    # otherwise check for updates at about 30 Hz
    time.sleep(0.033)
    return updateState

# STATE: Build the Program
# redirects to buildState if nothing has changed
# redirects to runProgramState if build succedded
# redirects to displayState if build failed
def buildState():
    global output

    # run the build process, in this case, "make"
    result = subprocess.run(['make'], encoding='utf8',
            stderr=subprocess.STDOUT, stdout = subprocess.PIPE)

    # if build succeeded, redirect to the run state
    if result.returncode == 0:
        return runProgramState

    # if build failed, save output and redirect to the error state
    if result.returncode == 2:
        output = result.stdout
        return displayState

    # else throw an error, this should never happen
    raise ("Unknown return value from build")

# STATE: Run the Program
# redirects to updateState if program output has not changed
# redirects to displayState on first run, or output changed
def runProgramState():
    global output

    result = subprocess.run('./build/a.out', encoding='utf8',
            stderr=subprocess.STDOUT, stdout = subprocess.PIPE)

    if result.stdout != output:
        output = result.stdout
        return displayState

    return updateState

# STATE: Display Output
# always prints output
# always redirects to updateState
def displayState():
    global output

    # feel free to skip clearing the console
    subprocess.call('clear')

    print(output)

    return updateState

# Needed to parse the file, then start the state machine loop
if __name__ == "__main__":
    stateMachine(buildState)
