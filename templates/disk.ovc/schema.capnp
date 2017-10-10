
@0xa5f2e16a4b6fc00b;
struct Schema {
	size @0 :Int64 = 1;
	type @1 :Text = "D";
	description @2 :Text = "disk";
	maxIOPS @3 :Int64 = 0;
	devicename @4 :Text;
	ssdSize @5 :Int64 = 10;
  g8client @6 :Text;
  location @7 :Text;
	totalBytesSec @8 :Int64;
  readBytesSec @9 :Int64;
	writeBytesSec @10 :Int64;
	totalIopsSec @11 :Int64;
  readIopsSec @12 :Int64;
	writeIopsSec @13 :Int64;
	totalBytesSecMax @14 :Int64;
	readBytesSecMax @15 :Int64;
  writeBytesSecMax @16 :Int64;
	totalIopsSecMax @17 :Int64;
	readIopsSecMax @18 :Int64;
  writeIopsSecMax @19 :Int64;
	sizeIopsSec @20 :Int64;
  diskId @21: Int64;
}
