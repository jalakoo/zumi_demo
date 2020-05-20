FROM alwaysai/edgeiq:0.12.0
RUN apt-get install libjpeg-dev && apt-get install zlib1g-dev && apt-get install libpng-dev
RUN pip install setuptools zumi
COPY update_zumi.sh /update_zumi.sh
RUN /bin/bash /update_zumi.sh