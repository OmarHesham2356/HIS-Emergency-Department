FROM archlinux:latest

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm \
        python \
        python-pip \
        mariadb-clients \
        make \
        && \
    pacman -Scc --noconfirm

COPY app/requirements.txt /tmp/requirements.txt
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ENV PATH="/opt/venv/bin:$PATH"
ENV PS1="(ed-his) $PS1"

WORKDIR /workdir
CMD ["sleep", "infinity"]
