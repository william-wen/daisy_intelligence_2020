#!/bin/bash

for file in $(cat files_done.txt); do
    mv flyer_images/$file processed_files/$file
done
