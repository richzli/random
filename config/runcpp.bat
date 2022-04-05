@echo off

:: run a c++ program by compiling, executing, then deleting the executable.

if exist %1 (
    g++ -Wall -o .cpp.%~n1.tmp %1 
    if ERRORLEVEL 1 (
        rem
    ) else (
        .cpp.%~n1.tmp
        del .cpp.%~n1.tmp
    )
) else (
    echo The specified file does not exist.
)
