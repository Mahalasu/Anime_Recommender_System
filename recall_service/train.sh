#!/bin/sh

if [ -z "${DATASET_PATH}" ]; then
    export DATASET_PATH="../data/"
fi

python -m bin.train