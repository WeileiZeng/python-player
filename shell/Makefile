# In extreme cold weather, the laptop is barely touchable. This cmd can heat the cpu for a while.
heat-cpu:
#	parallel -j20 echo hello  ::: {1..365} ::: {1..24}
	parallel -j20 echo Use cpu to heat your laptop  ::: {1..365}/365 ::: {1..24} ::: {1..60} ::: {1..60} ::: {1..10}
