#!/bin/sh

if [ -z "${RECALL_PORT}" ]; then
    export RECALL_PORT=5001
fi
if [ -z "${DATASET_PATH}" ]; then
    export DATASET_PATH="../data/"
fi

export FLASK_APP=setup

flask run -p $RECALL_PORT