#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h> // Added for timestamp

// Structure for Logger
typedef struct logger {
    int printEnabled;
    FILE* logfile;
    char* filename;
} Logger;

// Function to set the file for logging
void setFile(Logger* logger, char* filename);

// Function to log a string to file
void logToFile(Logger logger, char* stringToLog);