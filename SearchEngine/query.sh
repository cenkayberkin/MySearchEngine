#!/bin/bash
#Get directory of this file
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
python $SCRIPTPATH/query.py $1
