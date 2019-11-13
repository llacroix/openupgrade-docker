FROM ubuntu:bionic
LABEL maintainer="Odoo S.A. <info@odoo.com>"

# Generate locale C.UTF-8 for postgres and general locale data
ENV LANG C.UTF-8

ARG WK_CHK=db48fa1a043309c4bfe8c8e0e38dc06c183f821599dd88d4e3cea47c5a5d4cd3

# Install some dependencies python3.6
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            python3.6 \
            python3-wheel \
            python3-setuptools \
            python3-pip \
            libpython3.6 \
            curl \
            gnupg \
            libpq-dev \
            libsasl2-2 \
            libldap-2.4-2 \
        && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 \
        && update-alternatives --install /usr/bin/pip pip3 /usr/bin/pip3 1 \
        && curl -o wkhtmltox.deb -sSL https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb \
        && dpkg --force-depends -i wkhtmltox.deb\
        && apt-get -y install -f --no-install-recommends \
        && rm -rf /var/lib/apt/lists/* wkhtmltox.deb

# Install latest postgresql-client
RUN set -x; \
        echo 'deb https://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' > etc/apt/sources.list.d/pgdg.list \
        && export GNUPGHOME="$(mktemp -d)" \
        && repokey='B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8' \
        && gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "${repokey}" \
        && gpg --armor --export "${repokey}" | apt-key add - \
        && gpgconf --kill all \
        && rm -rf "$GNUPGHOME" \
        && apt-get update  \
        && apt-get install -y postgresql-client \
        && rm -rf /var/lib/apt/lists/*

# Install Odoo Including things from sources
ENV ODOO_VERSION 11.0
ARG ODOO_RELEASE=20190919
ARG ODOO_ARCHIVE=odoo-${ODOO_VERSION}.post${ODOO_RELEASE}
ARG URL=https://github.com/OCA/OpenUpgrade.git
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            build-essential \
            python3.6-dev \
            libsasl2-dev \
            libldap2-dev \
            git \
        && pip3 install \
            psycogreen \
        && git clone --depth 1 -b ${ODOO_VERSION} ${URL} /opt/odoo \
        && cd /opt/odoo \
        && echo 'recursive-include odoo *.py' >> MANIFEST.in \
        && echo 'recursive-include odoo *.txt' >> MANIFEST.in \
        && mv addons/* odoo/addons \
        && pip3 install . \
        && pip3 install --ignore-installed git+https://github.com/OCA/openupgradelib.git@master \
        && pip3 install -U "pyyaml == 3.12" \
        && pip3 install -U \
                xlrd \
                num2words \
        && apt-get --purge remove -y \
            build-essential \
            python3.6-dev \
            libsasl2-dev \
            libldap2-dev \
            git \
        && apt-get autoremove -y \
        && cd / \
        && rm -rf /opt/odoo \
        && rm -rf /var/lib/apt/lists/*

VOLUME /etc/odoo
VOLUME /var/lib/odoo

COPY ./odoo.conf /etc/odoo/
COPY ./entrypoint.py /

RUN groupadd -r -g 109 odoo \
    && useradd -r -u 105 -g odoo -b /var/lib -m odoo \
    && chown odoo /etc/odoo/odoo.conf

ENV ODOO_RC /etc/odoo/odoo.conf

USER odoo
ENTRYPOINT ["/entrypoint.py"]

cmd ["odoo"]
