#!/tools/Python/Python-2.7.3/bin/python2.7
##	by Han Bit Yoon (email: hanbit.yoon@gmail.com)
######################################################################################################### 
import sys
import os
import argparse
import subprocess

def main(args):

    T1 = args.t1
    ATLAS = args.atlas
    METRIC = args.metric
    TISSUE_SEG = args.tissueSeg
    VENT_MASK = args.ventricleMask
    OUTPUT_DIR = args.output

    T1_dir=os.path.dirname(T1)
    T1_base=os.path.splitext(os.path.basename(T1))[0]
    OUT_VENT_MASK = os.path.join(OUTPUT_DIR, "".join([T1_base,"_AtlasToVent.nrrd"]))
    SEG_WithoutVent = os.path.join(OUTPUT_DIR, "".join([T1_base,"_EMS_withoutVent.nrrd"]))
    ANTs_MATRIX_NAME=os.path.join(OUTPUT_DIR, T1_base)
    ANTs_WARP = os.path.join(OUTPUT_DIR, "".join([T1_base,"_Warp.nii.gz"]))
    ANTs_AFFINE = os.path.join(OUTPUT_DIR, "".join([T1_base,"_Affine.txt"]))

    os.system('ANTS 3 -m CC\\[%s, %s,1,4\\] -i 100x50x25 -o %s -t SyN\\[0.25\\] -r Gauss\\[3,0\\]' %(T1, ATLAS, ANTs_MATRIX_NAME) )

    args=['WarpImageMultiTransform', '3', VENT_MASK, OUT_VENT_MASK, ANTs_WARP, ANTs_AFFINE, '-R', T1, '--use-NN']
    warpImg = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = warpImg.communicate()

    args=['ImageMath', TISSUE_SEG, '-mul', OUT_VENT_MASK, '-outfile', SEG_WithoutVent]
    ImgMath = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = ImgMath.communicate()

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Calculates segmentation w/o ventricle mask. Computes deformation field with T1 vs ATLAS, applies warp to ventricle mask and masks tissue-seg')
    parser.add_argument('--t1', type=str, help='T1 Image to calculate deformation field against atlas', default="@T1IMG@")
    parser.add_argument('--atlas', type=str, help='Atlas image', default="@ATLAS@")
    parser.add_argument('-metric', type=str, help='Image Metric in ANTS (Check ANTS doc to set this parameter)', default="@IMAGEMETRIC@")
    parser.add_argument('--tissueSeg', type=str, help='Tissue Segmentation', default="@TISSUE_SEG@")
    parser.add_argument('--ventricleMask', type=str, help='Ventricle mask', default="@VENTRICLE_MASK@")
    parser.add_argument('--output', type=str, help='Output directory', default="@OUTPUT_DIR@")
    parser.add_argument('--outputName', type=str, help='Output masked tissue-seg', default="@OUTPUT_MASK@")
    args = parser.parse_args()
    main(args)
