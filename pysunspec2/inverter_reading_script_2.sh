#!/bin/bash
source /home/pai/Documents/sunspec_pai/bin/activate
python /home/pai/Documents/sunspec_pai/pysunspec2/inverter_reading.py -a 2 >> /home/pai/Documents/sunspec_pai/pysunspec2/inverter_reading_2_cron.log 2>&1
