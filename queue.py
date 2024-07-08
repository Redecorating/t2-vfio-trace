DEBUG_Q = False
REG_DOORBELL_BASE = 0x44000

def dissect_queue_write(offset, val):
	val = int.from_bytes(val)
	qid = (offset - REG_DOORBELL_BASE) // 4
	print(f"write doorbell qid={qid}, tail={val}")
def dissect_queue_read(offset, val):
	print('r', hex(offset),val)
