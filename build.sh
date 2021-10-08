cp Dockerfile.base Dockerfile && \
./command2label.py ./xnat/command.json >> Dockerfile && \
docker build -t xnat/model-datacsv:latest .
docker tag xnat/model-datacsv:latest registry.nrg.wustl.edu/docker/nrg-repo/yash/model-datacsv:latest
rm Dockerfile
