# geog5092-lab4
Lab 4 for GEOG 5092, Fall 2020

Completed by Mallory Prentiss

Scenario: You have been contracted to conduct a site suitability analysis for a wind farm in the Philippines. Based on wind resource data and a set of exclusions, you will identify potential sites forthe wind farm. You will then calculate the distance from potential sites to electricity grid transmission substations.

Overview: You will create a final suitability surface of potential sites for the wind farmby combining the raster layers. To do so, you need to create Boolean arrays for the five different selection criteria based on the thresholds specified below. You will develop a framework for conducting moving window operations. The dimensions of the moving window willbe 11km North-South by 9km East-West, producing 99km2 potential wind farm sites. Finally, you will calculate the Euclidean distance between the center of suitable sites and the closest transmission substation.

Selection Criteria: The following five conditionsfor the potential sitesare the basis for your suitability analysis:
1. The site cannot containurban areas.
2. Less than 2% of land can be covered by water bodies.
3. Less than 5% of the site can be within protected areas.
4. An average slope of less than 15 degrees is necessary for the development plans.
5. The average wind speedmust be greater than 8.5m/s.

Part I: Evaluate site suitability
1. Write a generic framework for calculating the mean value of a raster within a moving window, i.e., create a focal filter using NumPy:
   a. Create an empty output array to store the mean values.
   b. Loop  over  each  pixel  (each  row  and  column)  and  calculate  the  meanwithin  the  moving window. The window dimensions must be 11 rows by 9 columns. Ignore the edge         effect pixels.
   c. Assign the mean value to the center pixel of the moving window in the output array.
2. Evaluate each of the selection criteria to produce five separate Boolean arrays.
3. Create a surface of suitability valuesby summing the five Boolean arrays. Only sites with a score of 5 will be considered; create a final Boolean suitability array indicating the location of the selected sites.
4. Convert your final numpy suitability array to a geotif raster file for visualization purposes.
5. In a final print statement, report the number of locations you found with a score of five.

Part II: Calculate distance to transmission substationsand implement functions
1. Using the substation coordinates, calculate the Euclidean distance from the centroid of each suitable site (i.e.,  with  a  score  of  5) to  the  closest  transmission substation. Print  the shortest and longest distance to the closest transmission substation among all of the suitable sites, i.e., you will only print two distances. HINT: You can get the coordinates for the upper left corner of the extent using the arcpy Raster object. This  is  the  upper  left  corner,  not  the  centroid  location  of  the upper  left  pixel.  You  need  to  use the locationsof  cell  centroidsfor  distance  calculations.  How  can  you  get  the  centroid  location  for  the upper left pixel? One way to get the centroid locations for the suitable sites is to calculate the centroid locations  for  all  pixels  and  then  subset  those  locations  for  only  the  suitable  sites. Look  at  the numpy meshgrid function.
2. Effectively implement functions for reusability and overall organization.
