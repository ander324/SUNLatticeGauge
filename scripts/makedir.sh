#!/bin/bash

awk '{print $1}' tmp | ./setup_dir.py
