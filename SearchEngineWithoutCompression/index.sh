#!/bin/bash
#Get directory of this file
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
python $SCRIPTPATH/index.py $1 $2
