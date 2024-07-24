FROM ubuntu:24.10

RUN apt-get update && apt-get install -y \
    zsh \
    openssh-client \
    curl \
    git \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    pipx \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && curl -sS https://starship.rs/install.sh | sh -s -- --yes \
    && git clone https://github.com/pyenv/pyenv.git /home/ubuntu/.pyenv \
    && chown -R ubuntu:ubuntu /home/ubuntu/.pyenv


COPY --chown=ubuntu .zshrc /home/ubuntu
ENV ZSH_THEME starship

USER ubuntu

ENV PYENV_ROOT="/home/ubuntu/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"
ENV PATH="/home/ubuntu/.local/bin:$PATH"

RUN eval "$(pyenv init --path)" \
    && pyenv install 3.11.9 \
    && pyenv global 3.11.9  \
    && pipx ensurepath \
    && pipx install poetry --python $(which python) \
    && poetry config virtualenvs.create true \
    && poetry config virtualenvs.prefer-active-python true \
    && poetry config virtualenvs.in-project true

WORKDIR /workspace
COPY ../ ./

CMD ["tail", "-f", "/dev/null"]