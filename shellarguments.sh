#!/bin/bash

#Sample shell script to take action based on the arguments passed to the script

if [ "$3" = "CPUload" ]; then
  if [ "$1" = "OK" ]; then
    echo "Do some action"
  elif [ "$1" = "CRITICAL" ]; then
    if [ "$4" = "(Return code of 255 is out of bounds)" ]; then
      echo "Don't worry, be happy!"
    else
      echo "do some action here as well"
    fi
  else
    echo "not OK not CRITICAL SKIIPING"
  fi
elif [ "$3" = "HTTP" ]; then
  if [ "$1" = "CRITICAL" ]; then
    if [ "$4" = "(Return code of 255 is out of bounds)" ]; then
      echo "Don't worry, be happy!"
    else
      echo "do some action"
    fi
  else
    echo "Service is ok"
  fi
elif [ "$3" = "DOWN" ]; then
  if [ "$1" = "CRITICAL" ]; then
    if [ "$4" = "(Return code of 255 is out of bounds)" ]; then
      echo "Don't worry, be happy!"
    else
      echo "Do some action again"
    fi
  else
    echo "Machine is up"
  fi

else
  echo "Some other service alert"
fi