import gdal
import json
import numpy as np
import os

from gbdx_task_interface import GbdxTaskInterface

class ModifyColors(GbdxTaskInterface):

    def invoke(self):

        # Get color changes
        color_pairs = self.get_input_string_port('colors', default='False').split(';')
        changes = {}
        for color_pair in color_pairs:
            pre, post = color_pair.split(':')
            changes[pre] = post

        # Get transparency
        transparency = self.get_input_string_port('transparency', default='False')
    	if transparency == 'True':
    	    transparency = True
    	elif transparency == 'False':
    	    transparency = False
    	else:
    	    print 'Invalid transparency value!'
    	    return 0

        # Get image filename; if there are multiple files, pick one arbitrarily
        image_dir = self.get_input_data_port('image')
        filename = [os.path.join(dp, f) for dp, dn, fn in os.walk(image_dir) for f in fn if 'tif' in f][0]
        if filename is None:
            print 'Invalid filename!'
            return 0

        # Create output directory
        self.out_dir = self.get_output_data_port('output')
        os.makedirs(self.out_dir)

        print 'Read input image'
        drv = gdal.GetDriverByName('GTiff')
        ds = gdal.Open(filename)
        gt = ds.GetGeoTransform()
        srs = ds.GetProjectionRef()
        if ds.RasterCount >=3:
            red = ds.GetRasterBand(1).ReadAsArray()
            grn = ds.GetRasterBand(2).ReadAsArray()
            blu = ds.GetRasterBand(3).ReadAsArray()
        # if there is only one band, create three bands
        elif ds.RasterCount == 1:
            red = ds.GetRasterBand(1).ReadAsArray()
            grn = ds.GetRasterBand(1).ReadAsArray()
            blu = ds.GetRasterBand(1).ReadAsArray()

        print 'Change colors'
        for before in changes.keys():
            rb, gb, bb = map(int, before.split(','))
            ra, ga, ba = map(int, changes[before].split(','))
            where = (red == rb) & (grn == gb) & (blu == bb)
            red[where], grn[where], blu[where] = ra, ga, ba

        print 'Write output image'
        out_file = os.path.join(self.out_dir, 'output.tif')
        if transparency:
            alf = np.bitwise_or(np.bitwise_or(red, grn), blu)
            ds = drv.Create(out_file, red.shape[1], red.shape[0], 4, options=['COMPRESS=LZW'])
        else:
            ds = drv.Create(out_file, red.shape[1], red.shape[0], 3, options=['COMPRESS=JPEG'])

        ds.SetGeoTransform(gt)
        ds.SetProjection(srs)
        ds.GetRasterBand(1).WriteArray(red)
        ds.GetRasterBand(2).WriteArray(grn)
        ds.GetRasterBand(3).WriteArray(blu)
        if transparency:
            ds.GetRasterBand(4).WriteArray(alf)
            ds.GetRasterBand(4).SetColorInterpretation(gdal.GCI_AlphaBand)

        ds = None

	return 1


if __name__ == "__main__":
    with ModifyColors() as task:
        response = task.invoke()

    if response:
	print 'Done!'
