uname_s=$(uname -s)
dir_name="linux"
if [ "$uname_s" == "Darwin" ];then
	echo "MacOS"
	dir_name="darwin"
fi
BUILD_DIR=build/${dir_name}
mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}
cmake -DCMAK_BUILD_TYPE=Release -DBUILD_SHARE=ON -DBUILD_SAMPLES=OFF -DBUILD_TEST=OFF ../..
make -j4
make install
