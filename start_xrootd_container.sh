#!/bin/bash

USERNAME=$1
CONTAINER='/cvmfs/singularity.opensciencegrid.org/fermilab/fnal-dev-sl7:jsl'
TOKEN_FOLDER=$HOME/./local/run/user

echo "<< activate cvmfs locations >>"
cvmfs_config probe
cvmfs_config probe singularity.opensciencegrid.org
cvmfs_config probe fermilab.opensciencegrid.org
cvmfs_config probe uboone.opensciencegrid.org

echo "<< activate apptainer >>"
module load apptainer/1.2.4-suid

echo "<< make run folder for bearer tokens >>"
echo "mkdir -p ${TOKEN_FOLDER}"
mkdir -p ${TOKEN_FOLDER}

echo "<< start container. next: run setup_container.sh >>"
cmd="apptainer shell -B /cvmfs:/cvmfs -B /cluster/tufts:/cluster/tufts -B $HOME/./local/run/user:/run/user /cvmfs/singularity.opensciencegrid.org/fermilab/fnal-dev-sl7:jsl"
echo $cmd
$cmd


