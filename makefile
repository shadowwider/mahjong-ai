all:
	python3 build_cpp.py build_ext --inplace;
	python3 build_cpp.py clean --all;