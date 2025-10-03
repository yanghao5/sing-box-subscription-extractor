.PHONY: clean
run:
	python3 main.py 
clean:
	rm ./temp -rf
	rm config.json nodes.json