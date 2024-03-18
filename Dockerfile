FROM ubuntu:20.04

# Install System requirnment pakcages
RUN usermod -u 1000 www-data && groupmod -g 1000 www-data && \
        apt-get update && apt-get install -y python3 python3-pip python3-dev  \
        && mkdir /var/www && rm -rf /var/cache/apt/*

# Copy requirenments
COPY ["entrypoint.sh", "requirements.txt", "/"]

# Install python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY [".", "/var/www"]

RUN chmod +x /entrypoint.sh && chown -R www-data. /var/www

WORKDIR "/var/www"

ENTRYPOINT ["/entrypoint.sh"]
