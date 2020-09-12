all: sbc sbd

sbd: synthetic-benchmark-driver.cpp
	g++ synthetic-benchmark-driver.cpp -o sbd -lOpenCL -std=c++11 -g -llsb -L/nfs/home/tliu/libscibench/lib -I/nfs/home/tliu/libscibench/include

sbc: synthetic-benchmark-checker.cpp
	g++ synthetic-benchmark-checker.cpp -o sbc -lOpenCL -std=c++11

clean:
	rm sbd sbc
