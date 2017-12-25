#!/usr/bin/env bash
url="http://YOUR_SERVER_NAME_OR_IP:4444/predict?text=this%20is%20a%20news%20sample%20text%20about%20sports,%20and%20football%20in%20specific" # add more URLs here

for i in {0..10}
do
   # run the curl job in the background so we can start another job
   # and disable the progress bar (-s)
   echo "fetching $url"
   curl $url -s &
done
wait #wait for all background jobs to terminate