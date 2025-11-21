#!/bin/bash
source /home/pai/Documents/sunspec_pai/bin/activate
python /home/pai/Documents/sunspec_pai/pysunspec2/inverter_reading.py -a 1 >> /home/pai/Documents/sunspec_pai/pysunspec2/inverter_reading_1_cron.log 2>&1
