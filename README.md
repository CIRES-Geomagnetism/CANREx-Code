# CANREx-Code
Code used in the Magnetic Anomaly Grid and Associated Uncertainty from Marine Trackline Data: The Caribbean Alternative Navigation Reference Experiment (CANREx) paper

This code was written by Aamna Sirohey and is a custom built python code that was used for calculation of cell by cell statistics using the formulas given in the following paper that is set to be published in AGU Earth and Space:

***
Magnetic Anomaly Grid and Associated Uncertainty from Marine Trackline Data: The Caribbean Alternative Navigation Reference Experiment (CANREx)

R.W. Saltus 1, A. Chulliat 1, B. Meyer 2, M. Bates 3, and A. Sirohey 3

1 Cooperative Institute for Research in the Environmental Sciences, University of Colorado.

2 NOAA National Centers for Environmental Information.

3 Sander Geophysics Ltd.

Corresponding author: Rick Saltus (richard.saltus@colorado.edu)
***

This software is being shared for academic use only.

To run this code, you must run this python code in the same directory as a csv file that contains your data in the following 4 columns:

"X": Latitude "Y": Longitude "Z": Residual Magnetic Anomaly Value "uncertainty": Uncertainty/error in Z

    Create csv, ensure input coordinates are in lat/lon (epsg: 4326)
    Set output coordinste projection desired (we used UTM Zone 11 North, epsg: 32611)
    Set your desired grid cellsize (we used 4000, the same as EMAG2v3 cellsize of 2 arc-minutes)
    Enter the projected grid bounds

NOTES:

    This code does not currently run if the input coordinates are not longitude and latitude
    As the code does not automatically calculate the projected grid bounds, you will have to do this yourself. We opened up our data in Oasis Montaj, and projected the data using their tool to find the grid dimensions of the data and used those numbers in our code, for example.
