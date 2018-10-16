#!/tools/Python/Python-3.6.2/bin/python3
##	by Han Bit Yoon (email: hanbit.yoon@gmail.com)
######################################################################################################### 

import sys
import os
import argparse
import subprocess

def eprint(*args, **kwargs):
    #print errors function
    print(*args, file=sys.stderr, **kwargs)

def call_and_print(args):
    #external process calling function with output and errors printing
    print(">>>ARGS: "+"\n\t".join(args)+'\n')
    sys.stdout.flush()
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    out=out.decode('utf-8')
    err=err.decode('utf-8')
    if(out!=''):
        print(out+"\n")
        sys.stdout.flush()
    if(err!=''):
        eprint(err+'\n')
        sys.stderr.flush()
        print('\n'+args[0]+' : errors occured, see errors log for more details\n\n')
        sys.stdout.flush()
    else:
        print('\n'+args[0]+' : exit with success\n\n')
        sys.stdout.flush()

def main(args):
    print(">>>>>>>>>>>>>>>>RIGIDALIGN")
    sys.stdout.flush()
    T1 = args.t1
    T2 = args.t2
    ATLAS = args.atlas
    BRAINSFit=args.BRAINSFit
    OUTPUT_DIR = args.output

    T2_exists=True
    if (T2 == ""):
        T2_exists=False

    T1_dir=os.path.dirname(T1)

    T1_split=os.path.splitext(os.path.basename(T1))
    if (T1_split[1] == 'gz'):
        T1_base=os.path.splitext(T1_split[0])
    else:
        T1_base=T1_split[0]

    STX_T1 = os.path.join(OUTPUT_DIR, "".join([T1_base,"_stx.nrrd"]))

    if (T2_exists):
        T2_dir=os.path.dirname(T2)
        T2_split=os.path.splitext(os.path.basename(T2))
        if (T2_split[1] == 'gz'):
            T2_base=os.path.splitext(T2_split[0])
        else:
            T2_base=T2_split[0]
        STX_T2 = os.path.join(OUTPUT_DIR, "".join([T2_base,"_stx.nrrd"]))

    args=[BRAINSFit, '--fixedVolume', ATLAS, '--movingVolume', T1, '--outputVolume', STX_T1, '--useRigid',\
    '--initializeTransformMode', 'useCenterOfHeadAlign', '--outputVolumePixelType', 'short']
    call_and_print(args)

    if (T2_exists):
        args=[BRAINSFit, '--fixedVolume', STX_T1, '--movingVolume', T2, '--outputVolume', STX_T2, '--useRigid',\
        '--initializeTransformMode', 'useCenterOfHeadAlign', '--outputVolumePixelType', 'short']
        call_and_print(args)

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Calculates segmentation w/o ventricle mask. Computes deformation field with T1 vs ATLAS, applies warp to ventricle mask and masks tissue-seg')
    parser.add_argument('--t1', type=str, help='T1 Image to calculate deformation field against atlas', default="@T1IMG@")
    parser.add_argument('--t2', type=str, help='T2 Image to calculate deformation field against atlas', default="@T2IMG@")
    parser.add_argument('--atlas', type=str, help='Atlas image', default="@ATLAS@")
    parser.add_argument('--BRAINSFit', type=str, help='BRAINSFit executable path', default="@BRAINSFIT_PATH@")
    parser.add_argument('--output', type=str, help='Output directory', default="@OUTPUT_DIR@")
    args = parser.parse_args()
    main(args)