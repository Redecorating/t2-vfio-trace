cmd_log = []

DEBUG_MB = False
DEBUG_TS = False

REG_MBOX_OUT_BASE = 0x820
REG_MBOX_REPLY_COUNTER = 0x108
REG_MBOX_REPLY_BASE = 0x810
REG_TIMESTAMP_BASE = 0xC000

bce_msg_types = {
	0x7: 'REGISTER_COMMAND_SQ',
	0x8: 'REGISTER_COMMAND_CQ',
	0xb: 'REGISTER_COMMAND_QUEUE_REPLY',
	0xc: 'SET_FW_PROTOCOL_VERSION',
	0x14: 'SLEEP_NO_STATE',
	0x15: 'RESTORE_NO_STATE',
	0x16: 'POWEROFF MAYBE??',
	0x17: 'SAVE_STATE_AND_SLEEP',
	0x18: 'RESTORE_STATE_AND_WAKE',
	0x19: 'SAVE_STATE_AND_SLEEP_FAILURE',
	0x1a: 'SAVE_RESTORE_STATE_COMPLETE'
}

def decode_mb_msg(msg, is_reply):
	msg_type = int.from_bytes(msg) >> 58
	msg_val = int.from_bytes(msg) & 0x3FFFFFFFFFFFFFF
	try:
		msg_type = bce_msg_types[msg_type]
	except KeyError:
		msg_type = hex(msg_type)
	cmd_log.append((is_reply, msg_type, msg_val))
	
	
	return msg_type, hex(msg_val)

msg = b''
ts = b''
def dissect_mb_write(offset, val):
	global msg, ts
	if (offset == REG_MBOX_OUT_BASE):
		msg = val;
	elif (offset == REG_MBOX_OUT_BASE + 4):
		msg = val + msg
	elif (offset == REG_MBOX_OUT_BASE + 8):
		if (int.from_bytes(val) != 0):
			print(f"non zero write({hex(offset)}, {val.hex()})")
	elif (offset == REG_MBOX_OUT_BASE + 12):
		if (int.from_bytes(val) != 0):
			print(f"non zero write({hex(offset)}, {val.hex()})")
		# 6 bytes for message type, 58 bytes for arg
		print(f"mb send", decode_mb_msg(msg, False))
	elif (offset == REG_TIMESTAMP_BASE):
		ts = val + ts
		
		ts = int.from_bytes(ts, signed=True)
		if (ts == -4):
			print("timestamp inital start")
		elif (ts == -3):
			print("timestamp start")
		elif (ts == -2):
			print("timestamp stop")
		else:
			if DEBUG_TS:
				print(f"timestamp {(ts/1e9)}s")
	elif (offset == REG_TIMESTAMP_BASE+8):
		ts = val
	else:
		print(hex(offset))

def dissect_mb_read(offset, val):
	global msg, ts
	if (offset == REG_MBOX_REPLY_COUNTER):
		if DEBUG_MB:
			print("read reply ctr", (int.from_bytes(val)>>20)&0xf) # how many pending messages are there to recv
	elif (offset == REG_MBOX_REPLY_BASE):
		msg = val;
	elif (offset == REG_MBOX_REPLY_BASE + 4):
		msg = val + msg
	elif (offset == REG_MBOX_REPLY_BASE + 8):
		if (int.from_bytes(val) != 0):
			print(f"non zero read({hex(offset)}, {val.hex()})")
	elif (offset == REG_MBOX_REPLY_BASE + 12):
		if (int.from_bytes(val) != 0):
			print(f"non zero read({hex(offset)}, {val.hex()})")
		print(f"mb recv", decode_mb_msg(msg, True))
	elif (offset == REG_TIMESTAMP_BASE+8):
		
		val = int.from_bytes(val, signed=True)
		if (val == -4):
			print("recv timestamp inital start")
		elif (val == -3):
			print("recv timestamp start")
		elif (val == -2):
			print("recv timestamp stop")
		else:
			if DEBUG_TS:
				print(f"recv timestamp {(ts/1e9)}s")
	else:
		print("read", hex(offset), val)
	
