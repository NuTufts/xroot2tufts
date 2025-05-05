#!/bin/bash

USERNAME=$1

echo "<< setup uboone products folder and ups system >>"
source /cvmfs/uboone.opensciencegrid.org/products/setup_uboone.sh

echo "<< get kerberos ticket for fermilab username>>"
kinit ${USERNAME}@FNAL.GOV

echo "<< setup uboonecode >>"
UBCODE_VERSION="v10_04_07_05"
QUAL="e26:prof"
CMD="setup uboonecode $UBCODE_VERSION -q $QUAL"
echo $CMD
$CMD

echo "<< setup xrootd >>"
echo "setup xrootd v5_5_5a -q e26:p3915:prof"
setup xrootd v5_5_5a -q e26:p3915:prof

echo "<< get tufts cluster userid >>"
echo "uid: ${UID}"

echo "<< make bearer token folder >>"
echo "mkdir -p /run/user/${UID}/"
mkdir -p /run/user/${UID}

echo "<< get authentication token. you might have to go to a website and sign-in using fermilab services password >>"
htgettoken -a htvaultprod.fnal.gov -i uboone

echo "<< set environment variables >>"
export BEARER_TOKEN_FILE="/run/user/${UID}/bt_u${UID}"
export IFDH_TOKEN_ENABLE=1
echo "BEARER_TOKEN_FILE=${BEARER_TOKEN_FILE}"
echo "IFDH_TOKEN_ENABLE=1"


