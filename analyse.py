#!/usr/bin/python3
import sys

filename = sys.argv[1]
DEBUG=False

from mbox import dissect_mb_write, dissect_mb_read, cmd_log
from queue import dissect_queue_write, dissect_queue_read

def process_vfio_region_write(args):
	dev = args[1:13]
	args = args[14:]
	region, args = args.split("+")
	offset, val, length = args.split(", ")
	length = length.split(")")[0]
	offset = int(offset,16)
	val = int(val,16)
	length = int(length)
	val = val.to_bytes(length)
	if "region4" == region:
		dissect_mb_write(offset, val);
	elif region == "region2":
		dissect_queue_write(offset,val);
	else:
		print(region)
		panic

def process_vfio_region_read(args):
	dev = args[1:13]
	args = args[14:]
	region, args = args.split("+")
	offset, args = args.split(", ")
	length = args.split(")")[0]
	val = args.split("= ")[1]
	offset = int(offset,16)
	val = int(val,16)
	length = int(length)
	val = val.to_bytes(length)
	if "region4" == region:
		dissect_mb_read(offset, val);
	elif region == "region2":
		dissect_queue_read(offset,val);
	else:
		print(region)
		panic
for line in open(filename).readlines():
	line = line.strip()
	if ("0000:04:00.1" not in line):
		continue

	cmd = line.split(":")[1].split(" ")[0]
	pid, time = line.split(":")[0].split("@")
	args = " ".join(line.split(" ")[2:])

	if cmd == "vfio_region_write":
		process_vfio_region_write(args)
	elif cmd == "vfio_region_read":
		process_vfio_region_read(args)
	else:
		if DEBUG:
			print("UNHANDLED", cmd, args)





