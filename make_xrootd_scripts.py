import os,sys

def get_standard_samdef_filelist_name( samdef ):
    return f"filelist_{samdef}.txt"

def get_standard_xrootd_url_filename( samdef ):
    return f"xrootdurl_{samdef}.txt"

def make_filelist_from_samdef( samdef, filelist ):
    print("Getting list of files from samweb def: ",samdef)
    print("outputing list into: ",filelist)
    pdeffiles = os.popen(f'samweb list-definition-files {samdef}')
    nfiles = 0
    with open(filelist,'w') as f:
        ldef = pdeffiles.readlines()
        for l in ldef:
            l = l.strip()
            if ".root" in l:
                print(l,file=f)
                nfiles += 1
    print("Number of files saved to samdef filelist: ",nfiles)
    return nfiles

def convert_samdef_filelist_into_xrootd_url_list( samdef ):
    print("Convert samdef filelist into xrootd url list")
    samdef_filelist=get_standard_samdef_filelist_name( samdef )
    xrootd_filelist=get_standard_xrootd_url_filename( samdef )

    fsamdef = open(samdef_filelist,'r')
    llsamdef = fsamdef.readlines()
    fxrootd = open(xrootd_filelist,'w')

    dcachelist = []
    non_dcachelist = []
    
    for lsamdef in llsamdef:
        lsamdef = lsamdef.strip()
        pfileloc = os.popen(f'samweb locate-file {lsamdef}')
        llfileloc = pfileloc.readlines()
        try:
            lfileloc = llfileloc[0]
        except:
            print("Error querying location for ",lsamdef)
            continue
        lfileloc = lfileloc.strip()
        print(lfileloc)
        """
        expect output like:
        enstore:/pnfs/uboone/overlay/uboone/merged_dlreco/prod_v10_04_07_05/SURPRISE_Test_Samples_v10_04_07_05_Run4b_super_unified_reco2_BNB_nu_overlay/reco2/00/01/98/69(3186@fb6628l9)
        """
        fpath=f'{lfileloc}'
        if "enstore:" not in fpath:
            non_dcachelist.append(fpath)
            continue
        # change first part of path to use url
        fpath = fpath.replace("enstore:/pnfs/","root://fndca1.fnal.gov:1097/pnfs/fnal.gov/usr/")
        
        # remove tag at the end
        index = fpath.find("(")
        print("index: ",index)
        if index>0:
            fpath = fpath[:index]
        fpath += "/"+lsamdef
        print("xrootd-url: ",fpath)
        print(fpath,file=fxrootd)
        dcachelist.append(fxrootd)
    fxrootd.close()
    ndcache = len(dcachelist)
    n_nondcache = len(non_dcachelist)
    print("Number in dcache (enstore): ",ndcache)
    print("Number in non-dcache location: ",n_nondcache)
    print(ndcache)
        

def transfer_xrootd_filelist( xrootd_filelist, out_dir, folder_split=None ):
    fxrootd = open(xrootd_filelist,'r')
    lxrootd = fxrootd.readlines()
    nxfer = 0
    for l in lxrootd[:2]:
        l = l.strip()
        if folder_split is None:
            dest = os.path.basename(l)
            dest = out_dir+"/"+dest
        else:
            idx = l.find(folder_split)
            dest = l[idx+len(folder_split)+1:]
            dest = out_dir+"/"+dest

        print("dest: ",dest)
        if os.path.exists(dest):
            print("already exists: ",dest)
            continue
        else:
            pass
            
        dirname=os.path.dirname(dest)
        cmdmkdir="mkdir -p %s"%(dirname)
        print(cmdmkdir)

        cmd = "xrdcp %s %s"%(l,dest)
        print(cmd)
        nxfer += 1

    print("Number transferred: ",nxfer)
    return nxfer

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Make xrootd scripts')
    parser.add_argument('out_dir',type=str,help='Location to save files')
    parser.add_argument('--samdef',required=False,default=None,help='Use samedef to transfer')
    

    args = parser.parse_args()
    
    if args.samdef is not None:
        samdef_flist = get_standard_samdef_filelist_name
        #nfiles = make_filelist_from_samdef( args.samdef, samdef_flist )
        
        xrootd_filelist = get_standard_xrootd_url_filename( args.samdef )
        #convert_samdef_filelist_into_xrootd_url_list( args.samdef )
        
        transfer_xrootd_filelist( xrootd_filelist, args.out_dir, folder_split="/reco2/" )
        
    
