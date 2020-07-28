from synergy_file_reader import SynergyFile
from datetime import datetime
from pytest import mark
from os import path
import numpy as np

@mark.parametrize("filename",["columnwise_table.txt"])
def test_time_series(filename):
	data = SynergyFile(path.join("time_series",filename))
	assert len(data)==1
	read = data[0]
	
	assert read.metadata["Software Version"] == (3,2,1)
	assert read.metadata["Experiment File Path"] == r"C:\foo.xpt"
	assert read.metadata["Protocol File Path"] == r"C:\bar.prt"
	assert read.metadata["Plate Number"] == "Plate 1"
	assert read.metadata["Reader Type"] == "Synergy H1"
	assert read.metadata["Reader Serial Number"] == "18092726"
	assert read.metadata["Reading Type"] == "Reader"
	assert read.metadata["procedure"] == "foo\nbar\nquz"
	
	assert read.metadata["datetime"] == datetime(2020,7,23,17,40,7)
	
	assert read.channels == ["OD:600"]
	assert read.rows == list("ABCDEFGH")
	assert read.cols == list(range(1,13))
	
	assert read.times[0] == 9*60+10
	assert read.times[-1] == 17*3600+29*60+10
	assert np.all( np.diff(read.times)==10*60 )
	
	temps = read.temperatures["OD:600"]
	assert len(read.times) == len(temps)
	assert temps[ 0] == 30.0
	assert temps[-1] == 30.1
	assert temps[ 5] == 30.1
	
	assert read["B4" ,"OD:600"][2] == 0.084
	assert read["B",4,"OD:600"][2] == 0.084
	assert read["B",4         ][2] == 0.084
	assert read["B4"          ][2] == 0.084
	assert read["b4" ,"OD:600"][2] == 0.084
	
