#!/bin/bash
# If this file is in your project root dir `aai app deploy`
#   will copy this to the target device app root directory.
#   Then either run this on the target deployment device
#   with ./build_standalone.sh by direct ssh or by using 
#   `aai app shell --no-container` from your dev machine.

echo 'Image name for standalone file? (no spaces)'
read image_name

cp Dockerfile Dockerfile.standalone
echo ''>>Dockerfile.standalone
echo 'WORKDIR /app'>>Dockerfile.standalone
echo 'COPY . ./'>>Dockerfile.standalone
echo 'RUN pip3 install -r requirements.txt'>>Dockerfile.standalone
echo 'CMD ["python3", "app.py"]'>>Dockerfile.standalone

if docker build -t $image_name -f Dockerfile.standalone .; then
    echo 'Build complete'
    echo 'To run the image use: docker run --rm --network=host --privileged -v /dev:/dev '$image_name ' OR '
    echo './start_standalone.sh'
else
    echo 'Unknown problem building image. Exit status: $?'
fi

# Create convenience start script
echo '#!/bin/bash' >> start_standalone.sh
echo 'docker run --rm --network=host --privileged -v /dev:/dev '$image_name >> start_standalone.sh
chmod +x ./start_standalone.sh