# A State-Machine based C++ update checker

This set of files is an attempt at solving a hot-reloading problem for C++
programs that just output to the console without input.

This hopefully will be a portable solution, but it is only tested on Linux at
the moment.

You will need to have python3, g++ and make installed.

In order to setup your project, place state.py in the base directory of your
c++ project. Place all of your source files in ./src. All build results will be
loaded into ./build

run "python3 state.py" or give the script execute permissions and run
"./state.py"
