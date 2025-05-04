# xroot2tufts

Instructions and scripts for transferring files from FNAL to Tufts using xrootd.

We use xrootd operating inside MicroBooNE's development SL7 container. 
The container allows us to use the tool to setup the authentication tokens we need to transfer files.

Right now, we have rough notes for doing this.

1. From the login node, start-up a worker node.

   ```
   srun --pty -p wongjiradlab --time 8:00:00 bash
   ```

2. Activate cvmfs

   ```
   cvmfs_config probe
   cvmfs_config probe fermilab.opensciencegrid.org
   cvmfs_config probe uboone.opensciencegrid.org
   ```

3. Load apptainer

   ```
   module load apptainer/1.2.4-suid
   ```

4. Make a directory in your home folder on the cluster for the bearer tokens to be stored.

   ```
   mkdir -p $HOME/./local/run/
   ```

5. Start the apptainer container
   
   ```
   apptainer shell -B /cvmfs:/cvmfs -B /cluster/tufts:/cluster/tufts -B /cluster/home/[username]/.local/run:/run /cvmfs/singularity.opensciencegrid.org/fermilab/fnal-dev-sl7:jsl
   ```

6. Now that you are in the container, setup the environment to activate ups

   ```
   source /cvmfs/uboone.openscience.grid/products/setup_uboone.sh
   ```

7. Setup uboonecode (to indirectly setup jobsub_lite and xrootd)

   ```
   setup uboonecode v10_04_07_05 -q e26:prof
   ```

8. Renew your kerboros ticket (last 24 hours)

   ```
   kinit [fermilab username]@FNAL.GOV
   ```

9. Get a bearer token (for more info on tokens, see this [uboonecode wiki page](https://cdcvs.fnal.gov/redmine/projects/uboonecode/wiki/Token_Authentication)):

   ```
   htgettoken -a htvaultprod.fnal.gov -i uboone   
   ```

10. Now samweb should work. Get a definition and locate files

    * get samweb definition files. example: 
      ```
      samweb list-definition-files SURPRISE_Test_Samples_v10_04_07_05_Run4b_super_unified_reco2_BNB_nu_overlay_reco2_dlreco
      ```
    * get location of file. example: 
      ```
      samweb locate-file merged_dlreco_5a594698-70b4-4415-b2df-5dd962f077cf_merge_20250430185537.root
      ```
      The above returns:
      ```
      enstore:/pnfs/uboone/overlay/uboone/merged_dlreco/prod_v10_04_07_05/SURPRISE_Test_Samples_v10_04_07_05_Run4b_super_unified_reco2_BNB_nu_overlay/reco2/00/01/98/45(3186@fb6628l9)
      ```
   

11. Run command:

    ```
    > export BEARER_TOKEN_FILE=/run/user/<uid>/bt_u<uid>
    > export IFDH_TOKEN_ENABLE=1
    > BEARER_TOKEN=`cat $BEARER_TOKEN_FILE`
    > xrdcp root://fndca1.fnal.gov:1097/pnfs/fnal.gov/usr/uboone/overlay/uboone/merged_dlreco/prod_v10_04_07_05/SURPRISE_Test_Samples_v10_04_07_05_Run4b_super_unified_reco2_BNB_nu_overlay/reco2/00/01/98/45/merged_dlreco_5a594698-70b4-4415-b2df-5dd962f077cf_merge_20250430185537.root?authz=Bearer%20$BEARER_TOKEN .    
    ```
    
    Note that in the above, we had to transform the location by replacing `/pnfs/uboone` to `root://fndca1.fnal.gov:1097/pnfs/fnal.gov/usr`






